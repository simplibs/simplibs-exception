import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception.testing import assert_exception_class


def test_settings_error_basic_contract(subtests):
    """Runs the universal validation suite including custom hierarchy polymorphism."""
    assert_exception_class(
        subtests,
        SimpleExceptionSettingsError,
        expected_parents=SimpleExceptionInternalError,  # Garantuje správnou dědičnost a chytatelnost
    )


def test_str_contains_rendered_message():
    """Guarantees that string serialization successfully contains specific custom fields."""
    err = SimpleExceptionSettingsError(label="settings-label", problem="invalid option")
    text = str(err)

    assert "SETTINGS ERROR" in text
    assert "invalid option" in text