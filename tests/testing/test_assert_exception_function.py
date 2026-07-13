"""
Tests for assert_exception_function — validation of the main orchestration engine pipeline.
"""
import sys
import pytest

# We import the internal pytest outcome exception to catch explicit pytest.fail calls
from _pytest.outcomes import Failed

from simplibs.exception.testing.assert_exception_function import assert_exception_function


# -----------------------------------------------------------------------------
# Test Target Dummies
# -----------------------------------------------------------------------------

class CustomException(Exception):
    """Exception class that satisfies the simplibs-exception interface."""
    def __init__(self, message: str, error_name: str = "TEST_ERR"):
        self.message = message
        self.error_name = error_name
        super().__init__(message)


def functional_target_custom(value: str):
    """Routine that raises our custom exception type."""
    if value == "valid":
        return True
    raise CustomException(message="Invalid input detected", error_name="ERR_001")


class SubtestNoOpSpy:
    """Zero-overhead dummy tracking stub."""
    def test(self, name: str): return self
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_exception_function_full_pipeline():
    """Verify that all pipeline stages work with a custom exception implementing the interface."""
    spy = SubtestNoOpSpy()

    # Orchestrator runs: callable -> valid_params -> invalid_params -> deep_check
    exc = assert_exception_function(
        spy,
        functional_target_custom,
        exception_type=CustomException,
        invalid_params=("bad",),
        valid_params=("valid",),
        message="Invalid input detected",
        error_name="ERR_001",
        verbose=False
    )

    assert isinstance(exc, CustomException)
    assert exc.message == "Invalid input detected"
    assert exc.error_name == "ERR_001"


def test_exception_function_skip_deep_check():
    """Verify that deep_check=False bypasses field inspection, allowing incorrect metadata."""
    spy = SubtestNoOpSpy()

    # deep_check=False means the orchestrator won't complain about the wrong message
    exc = assert_exception_function(
        spy,
        functional_target_custom,
        exception_type=CustomException,
        invalid_params=("bad",),
        message="This message is intentionally WRONG and will be ignored",
        deep_check=False,
        verbose=False
    )

    assert isinstance(exc, CustomException)


def test_exception_function_fails_on_wrong_exception_type():
    """Verify that the negative gate correctly catches type mismatches."""
    spy = SubtestNoOpSpy()

    # -------------------------------------------------------------------------
    # Guard Interception Verification
    # -------------------------------------------------------------------------
    # We expect the internal Framework Guard to trigger a hard fail via pytest.fail().
    # This purposefully bypasses standard AssertionErrors to provide distinct diagnostic tips,
    # raising an internal '_pytest.outcomes.Failed' exception.
    with pytest.raises(Failed):
        assert_exception_function(
            spy,
            functional_target_custom,
            exception_type=ValueError,  # Intentionally wrong type to trigger the guard
            invalid_params=("bad",),
            verbose=False
        )