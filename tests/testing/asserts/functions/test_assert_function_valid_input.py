"""
Tests for assert_function_valid_input — validation of positive execution paths and signature routing.
"""
import pytest
from simplibs.exception.testing.asserts.functions.assert_function_valid_input import assert_function_valid_input
from simplibs.exception.testing.tools import Kwargs


# -----------------------------------------------------------------------------
# Test Target Dummies
# -----------------------------------------------------------------------------

def successful_function(*args, **kwargs):
    """A routine that always succeeds."""
    return "success"


def failing_function(*args, **kwargs):
    """A routine that always raises an error."""
    raise RuntimeError("Unexpected failure")


class SubtestNoOpSpy:
    """Mock spy bypassing the native pytest-subtests overhead during core testing."""

    def test(self, name: str): return self

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb): return False


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_valid_input_passes_with_correct_payload():
    """Verify that execution proceeds cleanly when valid parameters are provided."""
    spy = SubtestNoOpSpy()

    # Should not raise anything
    assert_function_valid_input(spy, successful_function, valid_params=("arg1",), verbose=False)


def test_valid_input_fails_when_function_raises_exception():
    """Verify that pytest captures the exception if the function fails unexpectedly."""
    spy = SubtestNoOpSpy()

    # We expect an exception here because failing_function is hardcoded to raise RuntimeError
    with pytest.raises(RuntimeError):
        assert_function_valid_input(spy, failing_function, valid_params=("arg1",), verbose=False)


def test_valid_input_handles_kwargs_via_process_params():
    """Verify that complex parameter normalization works correctly using the core router."""
    spy = SubtestNoOpSpy()

    # Testing with a dummy function that checks if kwargs are passed
    def verify_kwargs(**kwargs):
        assert kwargs["key"] == "value"

    # We rely on process_params to handle the Kwargs object conversion
    assert_function_valid_input(spy, verify_kwargs, valid_params=Kwargs(key="value"), verbose=False)