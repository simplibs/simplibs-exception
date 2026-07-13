"""
Tests for raise_unknown_settings_attribute_error — validation of dynamic reflection gates for settings attributes.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.SettingsMeta import SettingsMeta
from simplibs.exception._core_logic.settings_meta.validations.raise_unknown_settings_attribute_error import (
    raise_unknown_settings_attribute_error,
)
from simplibs.exception.testing import assert_exception_function


# -----------------------------------------------------------------------------
# Invalid Input Matrix — Reflection & Attribute Resolution
# -----------------------------------------------------------------------------

def test_raise_unknown_settings_attribute_error(subtests):
    """Verify that the raiser terminates execution with a precise, fully-populated internal error."""
    # Dynamically resolve public permitted keys to match the active internal state of SettingsMeta
    permitted_keys = [k for k in SettingsMeta._VALIDATORS if not k.startswith("_")]

    assert_exception_function(
        subtests,
        raise_unknown_settings_attribute_error,
        invalid_params=(SettingsMeta, "bad-value"),
        exception_type=SimpleExceptionSettingsError,
        value="bad-value",
        label="SimpleExceptionSettings",
        expected=f"one of the permitted attributes: {permitted_keys}",
        problem="unknown attribute — likely a typo or a new attribute missing its validator",
        how_to_fix=(
            "Check for a typo — the permitted operational attributes are listed under 'Expected'.",
            "If introducing a new setting, register its corresponding validation block inside _VALIDATORS.",
        ),
    )