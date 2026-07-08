"""
Tests for assert_exception_function — functional intercept gates, parameter unpacking, and telemetry auditing.
"""
import pytest
from _pytest.outcomes import Failed
from simplibs.sentinels import UNSET
from simplibs.exception.testing.assert_exception_function import assert_exception_function


# -----------------------------------------------------------------------------
# Test Doubles & Mocks
# -----------------------------------------------------------------------------

class DummyCustomException(BaseException):
    """Custom exception double for testing interception boundaries."""
    def __init__(self, **kwargs):
        # Set fields directly for check_exception_fields audit compatibility
        self.error_name = kwargs.get("error_name", "DUMMY_ERROR")
        self.value = kwargs.get("value", None)


class SubtestSpy:
    """Mock mirroring pytest-subtests engine to track sequence checkpoint execution."""
    def __init__(self):
        self.called_subtests = []

    def test(self, name):
        self.called_subtests.append(name)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


# -----------------------------------------------------------------------------
# Core Execution Target Mocks
# -----------------------------------------------------------------------------

def mock_validator_function(age: int) -> None:
    """Simulates a business logic gate that requires a positive integer."""
    if age < 0:
        raise DummyCustomException(error_name="INVALID_AGE", value=age)


def mock_no_raise_function(age: int) -> None:
    """Flawed function that never raises an exception, used to test interception failure."""
    pass


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_full_pipeline_success_with_valid_and_invalid_params():
    """Verify happy/sad path execution, argument unpacking, and telemetry verification loops."""
    spy = SubtestSpy()

    # Run the orchestrator against the compliant validator
    captured_exc = assert_exception_function(
        subtests=spy,
        func=mock_validator_function,
        valid_param=25,              # Happy path parameter
        invalid_param=-5,            # Sad path parameter
        exception_type=DummyCustomException,
        error_name="INVALID_AGE",    # Telemetry criteria
        value=-5,
        verbose=True
    )

    # 1. Ensure the correct raised instance was returned
    assert isinstance(captured_exc, DummyCustomException)
    assert captured_exc.error_name == "INVALID_AGE"
    assert captured_exc.value == -5

    # 2. Verify all multi-stage pipeline subtests were triggered sequentially
    assert "test_callable" in spy.called_subtests
    assert "test_valid_input" in spy.called_subtests
    assert "test_raises_exception" in spy.called_subtests

    # 3. Verify that check_exception_fields registered fields subtests
    assert "test_error_name" in spy.called_subtests
    assert "test_value" in spy.called_subtests


def test_happy_path_skipped_if_valid_param_is_unset():
    """If valid_param is UNSET, the happy path validation pass must be bypassed completely."""
    spy = SubtestSpy()

    assert_exception_function(
        subtests=spy,
        func=mock_validator_function,
        invalid_param=-10,
        exception_type=DummyCustomException,
        error_name="INVALID_AGE"
    )

    assert "test_callable" in spy.called_subtests
    assert "test_valid_input" not in spy.called_subtests  # Muted!
    assert "test_raises_exception" in spy.called_subtests


def test_interception_gate_failure_when_exception_is_not_raised():
    """If the target function fails to raise any exception under invalid parameters, it must fail."""
    spy = SubtestSpy()

    # mock_no_raise_function won't crash on invalid_param, so pytest.raises will throw a Failed exception
    with pytest.raises(Failed):
        assert_exception_function(
            subtests=spy,
            func=mock_no_raise_function,
            invalid_param=-5,
            exception_type=DummyCustomException
        )