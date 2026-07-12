import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionModeError import (
    SimpleExceptionModeError,
)
from simplibs.exception.testing import assert_exception_class


def test_mode_error_basic_contract(subtests):
    """Runs the universal validation suite including custom hierarchy polymorphism."""
    assert_exception_class(
        subtests,
        SimpleExceptionModeError,
        expected_parents=SimpleExceptionInternalError,  # Garantuje správnou dědičnost a chytatelnost
    )


def test_str_contains_rendered_message():
    """Guarantees that string serialization successfully contains specific custom fields."""
    err = SimpleExceptionModeError(label="mode-label", problem="invalid data contract")
    text = str(err)

    assert "MODE ERROR" in text
    assert "invalid data contract" in text