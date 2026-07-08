import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionModeError import (
    SimpleExceptionModeError,
)


def test_is_subclass_of_internal_error():
    """Ensures that ModeError correctly inherits from the central InternalError group base class."""
    assert issubclass(SimpleExceptionModeError, SimpleExceptionInternalError)


def test_default_error_name():
    """Validates that the class correctly overrides its declarative identity to MODE ERROR."""
    err = SimpleExceptionModeError(label="x")
    assert err.error_name == "MODE ERROR"


def test_can_be_raised_and_caught_as_internal_error():
    """
    Verifies polymorphism inside the internal exception hierarchy: a ModeError
    must be catchable via a generic SimpleExceptionInternalError block.
    """
    with pytest.raises(SimpleExceptionInternalError):
        raise SimpleExceptionModeError(label="bad mode")


def test_str_contains_rendered_message():
    """
    Guarantees that string serialization successfully inherits the PRETTY layout mapping
    and outputs all specific error identity parameters.
    """
    # 1. Instantiate error payload with specific presentation faults
    err = SimpleExceptionModeError(label="mode-label", problem="invalid data contract")
    text = str(err)

    # 2. Assert structural visual text block contents
    assert "MODE ERROR" in text
    assert "invalid data contract" in text


def test_exception_trapping_hierarchy_order():
    """
    Architectural Contract: Verifies the exact MRO trapping sequence. A specialized
    ModeError must trigger the first matching specific except block, preventing
    it from leaking immediately into a generic fallback internal error catch block.
    """
    triggered_specific = False
    triggered_generic = False

    try:
        raise SimpleExceptionModeError(label="test-mro")
    except SimpleExceptionModeError:
        triggered_specific = True
    except SimpleExceptionInternalError:
        triggered_generic = True

    assert triggered_specific is True
    assert triggered_generic is False