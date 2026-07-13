"""
Tests for raise_system_blacklist_mutation_error — validation of internal system-level protection gates.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.raise_system_blacklist_mutation_error import (
    raise_system_blacklist_mutation_error,
)
from simplibs.exception.testing import assert_exception_function


# -----------------------------------------------------------------------------
# Invalid Input Matrix — System Metadata Protection Guards
# -----------------------------------------------------------------------------

def test_raise_system_blacklist_mutation_error(subtests):
    """Verify that the raiser terminates execution with a precise, fully-populated internal error."""
    assert_exception_function(
        subtests,
        raise_system_blacklist_mutation_error,
        invalid_params=("bad-value",),
        exception_type=SimpleExceptionSettingsError,
        value="bad-value",
        label="SimpleExceptionSettings",
        problem="The protected '_SYSTEM_BLACKLIST' attribute is strict read-only metadata.",
        how_to_fix=(
            "Do not attempt to alter the core framework system-level blacklist.",
            "To skip your custom repository paths or wrapper files, append them to: "
            "SimpleExceptionSettings.LOCATION_BLACKLIST",
        ),
    )