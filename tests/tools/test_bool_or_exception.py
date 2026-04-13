"""
Tests for bool_or_exception — boolean return mode, exception raising mode, and get_location increment logic.
"""
import pytest
from simplibs.exception.tools.bool_or_exception import bool_or_exception
from simplibs.exception.SimpleException import SimpleException


# -----------------------------------------------------------------------------
# Boolean return mode
# -----------------------------------------------------------------------------

def test_returns_false_when_return_bool_is_true():
    """If return_bool is True, the function must return False and NOT raise an exception."""
    result = bool_or_exception(return_bool=True)
    assert result is False


def test_returns_false_even_with_other_kwargs():
    """If return_bool is True, kwargs are ignored and False is returned."""
    result = bool_or_exception(return_bool=True, message="Error message", value=123)
    assert result is False


# -----------------------------------------------------------------------------
# Exception raising mode
# -----------------------------------------------------------------------------

def test_raises_simple_exception_when_return_bool_is_false():
    """If return_bool is False, SimpleException must be raised."""
    with pytest.raises(SimpleException):
        bool_or_exception(return_bool=False)


def test_kwargs_are_passed_to_exception():
    """kwargs must be forwarded to SimpleException — verified via instance attribute."""
    test_message = "Custom error message"
    with pytest.raises(SimpleException) as exc_info:
        bool_or_exception(return_bool=False, message=test_message)
    assert exc_info.value.message == test_message


# -----------------------------------------------------------------------------
# get_location increment logic
# -----------------------------------------------------------------------------

def test_get_location_is_incremented_by_one_for_positive_int():
    """get_location > 0 must be incremented by 1 before passing to SimpleException."""
    with pytest.raises(SimpleException) as exc_info:
        bool_or_exception(return_bool=False, get_location=2)
    assert exc_info.value._get_location == 3


def test_get_location_zero_is_not_incremented():
    """get_location=0 must NOT be incremented — boundary of the > 0 condition."""
    with pytest.raises(SimpleException) as exc_info:
        bool_or_exception(return_bool=False, get_location=0)
    assert exc_info.value._get_location == 0


def test_get_location_non_int_is_not_incremented():
    """A non-int get_location must be passed through unchanged."""
    with pytest.raises(SimpleException) as exc_info:
        bool_or_exception(return_bool=False, get_location=False)
    assert exc_info.value._get_location == False