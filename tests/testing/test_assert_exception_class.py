"""
Tests for assert_exception_class — public instantiation auditing, parameter forwarding, and instance retrieval.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.testing.assert_exception_class import assert_exception_class


# -----------------------------------------------------------------------------
# Test Doubles & Mocks
# -----------------------------------------------------------------------------

class DummyExceptionBlueprint:
    """Mock exception class capturing any kwargs passed during instantiation."""
    def __init__(self, **kwargs):
        self.kwargs_at_init = kwargs
        # Set attributes directly so check_exception_fields can read them
        for k, v in kwargs.items():
            setattr(self, k, v)


class StaticMismatchExceptionBlueprint:
    """Mock exception that forces a fixed value to simulate a state breach in tests."""
    def __init__(self, **kwargs):
        # We explicitly ignore what was passed and lock a fixed value
        self.problem = "static_original_text"
        self.error_name = "STATIC_ERROR"


class SubtestSpy:
    """Mock mirroring pytest-subtests engine to track registered checkpoints."""
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
# Unit Tests
# -----------------------------------------------------------------------------

def test_instantiation_and_parameter_forwarding():
    """Verify that assert_exception_class initializes the exception blueprint and transfers parameters."""
    spy = SubtestSpy()

    # Execute the public helper with a curated subset of fields
    exc_instance = assert_exception_class(
        subtests=spy,
        exc_class=DummyExceptionBlueprint,
        error_name="CUSTOM_ERROR",
        value=42,
        problem="invalid constant",
        exact_match=True,
        verbose=True,
        intro="manual_"
    )

    # 1. Verify that the function returned the correct live instance
    assert isinstance(exc_instance, DummyExceptionBlueprint)

    # 2. Verify defensive sentinel-to-None transformation logic during construction
    assert exc_instance.kwargs_at_init["error_name"] == "CUSTOM_ERROR"
    assert exc_instance.kwargs_at_init["value"] == 42
    assert exc_instance.kwargs_at_init["problem"] == "invalid constant"
    assert exc_instance.kwargs_at_init["label"] is None  # UNSET turns into None inside init
    assert exc_instance.kwargs_at_init["oneline"] is False  # UNSET turns into False inside init

    # 3. Verify that verification routed through check_exception_fields and registered subtests
    assert "manual_test_error_name" in spy.called_subtests
    assert "manual_test_value" in spy.called_subtests
    assert "manual_test_problem" in spy.called_subtests


def test_assertion_failure_bubbles_up_on_mismatch():
    """Verify that if an instantiated exception state violates expectations, an error is raised."""
    spy = SubtestSpy()

    # The exception will have problem="static_original_text", but we expect something else.
    # This must reliably trigger an AssertionError.
    with pytest.raises(AssertionError):
        assert_exception_class(
            subtests=spy,
            exc_class=StaticMismatchExceptionBlueprint,
            problem="completely_different_expected_text",
            exact_match=True
        )