"""
Tests for validate_message_mode — runtime validation of framework presentation layout modes.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_message_mode import (
    validate_message_mode,
)
from simplibs.exception.modes.LOG import LOG
from simplibs.exception.modes.PRETTY import PRETTY
from simplibs.exception.modes.SIMPLE import SIMPLE
from simplibs.exception.modes.base_class.ModeBase import ModeBase
from simplibs.exception.testing import assert_exception_function
from simplibs.exception.testing.asserts.functions.assert_function_valid_input import assert_function_valid_input


# Mocking a valid user-defined extension for architectural verification
class CustomJsonFormattingMode(ModeBase):
    """A custom external layout engine designed by an ecosystem consumer."""
    def _render(self, *args, **kwargs):
        return "mock-rendered-string"


# -----------------------------------------------------------------------------
# 1. Valid Input Matrix — Built-in Singletons & Extensions
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("valid_mode", [
    PRETTY,
    SIMPLE,
    LOG,
    CustomJsonFormattingMode()
])
def test_validate_message_mode_valid_inputs(subtests, valid_mode):
    """Verify that the validator permits all built-in singletons and valid user-defined ModeBase extensions."""
    assert_function_valid_input(
        subtests,
        validate_message_mode,
        valid_params=(valid_mode,),  # Safe encapsulation into the execution tuple
        verbose=False
    )


# -----------------------------------------------------------------------------
# 2. Invalid Input Matrix — Type & Structure Violations
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("invalid_mode", [
    "not-a-mode",
    12345,
    ModeBase,  # Raw blueprint class passed instead of a fully formed engine instance
])
def test_validate_message_mode_invalid_inputs(subtests, invalid_mode):
    """Verify that any non-ModeBase payload triggers a strict structural layout configuration error."""
    assert_exception_function(
        subtests,
        validate_message_mode,
        invalid_params=(invalid_mode,),  # Encapsulated on-the-fly into execution tuple
        valid_params=(SIMPLE,),           # Gold-standard verification using a valid built-in singleton
        exception_type=SimpleExceptionSettingsError,
        value=invalid_mode,               # Pure un-wrapped payload passed for exact attribute matching
        label="MESSAGE_MODE",
        expected="an instance of a class derived from ModeBase (e.g., PRETTY, SIMPLE, ONELINE, LOG)",
        problem="value is not a valid framework output mode configuration",
        how_to_fix=(
            "Use one of the pre-configured built-in singletons: PRETTY, SIMPLE, ONELINE, LOG.",
            "If building a custom formatting engine, ensure it inherits strictly from ModeBase.",
        ),
    )