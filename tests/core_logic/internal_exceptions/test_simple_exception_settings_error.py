import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)


def test_is_subclass_of_internal_error():
    """Ensures that SettingsError correctly inherits from the central InternalError group base class."""
    assert issubclass(SimpleExceptionSettingsError, SimpleExceptionInternalError)


def test_default_error_name():
    """Validates that the class correctly overrides its declarative identity to SETTINGS ERROR."""
    err = SimpleExceptionSettingsError(label="x")
    assert err.error_name == "SETTINGS ERROR"


def test_can_be_raised_and_caught_as_internal_error():
    """
    Verifies polymorphism inside the internal exception hierarchy: a SettingsError
    must be catchable via a generic SimpleExceptionInternalError block.
    """
    with pytest.raises(SimpleExceptionInternalError):
        raise SimpleExceptionSettingsError(label="bad setting")


def test_str_contains_rendered_message():
    """
    Guarantees that string serialization successfully inherits the PRETTY layout mapping
    and outputs all specific configuration error parameters.
    """
    # 1. Instantiate error payload with specific configuration faults
    err = SimpleExceptionSettingsError(label="settings-label", problem="invalid option")
    text = str(err)

    # 2. Assert structural visual text block contents
    assert "SETTINGS ERROR" in text
    assert "invalid option" in text


def test_isolated_from_global_settings_state():
    """
    Architectural Edge Case: Verifies that the exception can be instantiated
    and formatted even with entirely stripped parameters, confirming it does not
    rely on external global state layers during a catastrophic boot failure.
    """
    # Instantiating with absolute bare minimums to check complete decoupling
    err = SimpleExceptionSettingsError()
    text = str(err)

    assert "SETTINGS ERROR" in text
    assert err.skip_locations == ()