"""
Tests for SimpleExceptionSettingsError — identity validation and configuration layer hierarchy.
"""
import pytest
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import SimpleExceptionSettingsError
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import SimpleExceptionInternalError


def test_settings_error_identity_and_formatting():
    """Verify that SimpleExceptionSettingsError overrides identity and renders it correctly."""
    error = SimpleExceptionSettingsError(problem="invalid truncation length")

    # Verify exact error name identity
    assert error.error_name == "SETTINGS ERROR"

    # Verify that the inherited PRETTY rendering layer includes this specific identity
    assert "SETTINGS ERROR" in str(error)
    assert "invalid truncation length" in str(error)


def test_settings_error_catching_hierarchy():
    """Verify the operational catching patterns from the design specification."""
    error = SimpleExceptionSettingsError(problem="configuration validation breach")

    # 1. Must be catchable via its specific class
    with pytest.raises(SimpleExceptionSettingsError):
        raise error

    # 2. Must be catchable via the generic internal base class boundary
    with pytest.raises(SimpleExceptionInternalError):
        raise error