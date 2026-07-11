import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.testing.asserts.asserts_functions.assert_function_raises import assert_function_raises


# -----------------------------------------------------------------------------
# Test Target Dummies
# -----------------------------------------------------------------------------

def function_that_fails(value):
    if value == "trigger_error":
        raise ValueError("Invalid value provided")
    if value == "trigger_type_error":
        raise TypeError("Wrong type")
    return "success"


class SubtestNoOpSpy:
    def test(self, name: str): return self

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb): return False


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_raises_catches_any_exception_when_unset():
    """Verify that it catches any BaseException when exception_type is UNSET."""
    spy = SubtestNoOpSpy()

    # Passing "trigger_error" should raise ValueError (which is a BaseException)
    exc = assert_function_raises(spy, function_that_fails, invalid_param=("trigger_error",), exception_type=UNSET)

    assert isinstance(exc, ValueError)
    assert str(exc) == "Invalid value provided"


def test_raises_verifies_correct_exception_type():
    """Verify that it successfully validates the specific exception type."""
    spy = SubtestNoOpSpy()

    # Should pass because TypeError matches
    exc = assert_function_raises(spy, function_that_fails, invalid_param=("trigger_type_error",), exception_type=TypeError)
    assert isinstance(exc, TypeError)


def test_raises_fails_on_incorrect_exception_type():
    """Verify that it raises an assertion error if the raised type doesn't match the expectation."""
    spy = SubtestNoOpSpy()

    # Expecting ValueError, but function raises TypeError
    with pytest.raises(AssertionError):
        assert_function_raises(spy, function_that_fails, invalid_param=("trigger_type_error",), exception_type=ValueError)


def test_raises_fails_if_no_exception_is_raised():
    """Verify that it fails if the function completes successfully."""
    spy = SubtestNoOpSpy()

    # function returns "success", so pytest.raises(BaseException) will fail
    with pytest.raises(pytest.fail.Exception):  # Pytest raises failure if no exception occurs
        assert_function_raises(spy, function_that_fails, invalid_param=("valid_input",), exception_type=UNSET)