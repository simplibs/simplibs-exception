import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)


def test_is_subclass_of_internal_error():
    assert issubclass(SimpleExceptionSettingsError, SimpleExceptionInternalError)


def test_default_error_name():
    err = SimpleExceptionSettingsError(label="x")
    assert err.error_name == "SETTINGS ERROR"


def test_can_be_raised_and_caught_as_internal_error():
    with pytest.raises(SimpleExceptionInternalError):
        raise SimpleExceptionSettingsError(label="bad setting")


def test_str_contains_rendered_message():
    err = SimpleExceptionSettingsError(label="settings-label", problem="invalid option")
    text = str(err)
    assert "SETTINGS ERROR" in text
    assert "invalid option" in text
