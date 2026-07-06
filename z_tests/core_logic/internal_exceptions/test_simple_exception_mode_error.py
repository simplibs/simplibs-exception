"""
Tests for SimpleExceptionModeError — identity validation and exception hierarchy integrity.
"""
import pytest
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionModeError import SimpleExceptionModeError
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import SimpleExceptionInternalError


def test_mode_error_identity_and_formatting():
    """Verify that SimpleExceptionModeError overrides identity and renders it correctly."""
    error = SimpleExceptionModeError(problem="invalid layout object")

    # Verify exact error name identity
    assert error.error_name == "MODE ERROR"

    # Verify that the inherited PRETTY rendering layer includes this specific identity
    assert "MODE ERROR" in str(error)
    assert "invalid layout object" in str(error)


def test_mode_error_catching_hierarchy():
    """Verify the operational catching patterns from the design specification."""
    error = SimpleExceptionModeError(problem="interface breach")

    # 1. Must be catchable via its specific class
    with pytest.raises(SimpleExceptionModeError):
        raise error

    # 2. Must be catchable via the generic internal base class boundary
    with pytest.raises(SimpleExceptionInternalError):
        raise error