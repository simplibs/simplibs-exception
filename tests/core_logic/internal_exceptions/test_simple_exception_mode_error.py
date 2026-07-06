import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionModeError import (
    SimpleExceptionModeError,
)


def test_is_subclass_of_internal_error():
    assert issubclass(SimpleExceptionModeError, SimpleExceptionInternalError)


def test_default_error_name():
    err = SimpleExceptionModeError(label="x")
    assert err.error_name == "MODE ERROR"


def test_can_be_raised_and_caught_as_internal_error():
    with pytest.raises(SimpleExceptionInternalError):
        raise SimpleExceptionModeError(label="bad mode")


def test_str_contains_rendered_message():
    err = SimpleExceptionModeError(label="mode-label", problem="invalid data contract")
    text = str(err)
    assert "MODE ERROR" in text
    assert "invalid data contract" in text
