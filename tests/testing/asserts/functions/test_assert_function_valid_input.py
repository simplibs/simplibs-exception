import pytest
from simplibs.exception.testing.asserts.asserts_functions.assert_function_valid_input import assert_function_valid_input


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
    assert_function_valid_input(spy, successful_function, valid_param=("arg1",), verbose=False)


def test_valid_input_fails_when_function_raises_exception():
    """Verify that pytest captures the exception if the function fails unexpectedly."""
    spy = SubtestNoOpSpy()

    # We expect an exception here because failing_function is hardcoded to raise RuntimeError
    with pytest.raises(RuntimeError):
        assert_function_valid_input(spy, failing_function, valid_param=("arg1",), verbose=False)


def test_valid_input_handles_kwargs_via_manage_param():
    """Verify that complex parameter normalization works correctly."""
    spy = SubtestNoOpSpy()

    # Testing with a dummy function that checks if kwargs are passed
    def verify_kwargs(**kwargs):
        assert kwargs["key"] == "value"

    # We rely on manage_param to handle the Kwargs object conversion
    # Assuming standard Kwargs usage:
    from simplibs.exception.testing.containers import Kwargs
    assert_function_valid_input(spy, verify_kwargs, valid_param=Kwargs(key="value"), verbose=False)