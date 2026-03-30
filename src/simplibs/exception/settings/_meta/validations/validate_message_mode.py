# Commons
from ....modes.base_class import ModeBase
# Inners
from .SimpleExceptionSettingsError import SimpleExceptionSettingsError


def validate_message_mode(value):
    """Verifies that the value is an instance of a class derived from ModeBase."""
    if not isinstance(value, ModeBase):
        raise SimpleExceptionSettingsError(
            value       = value,
            value_label = "DEFAULT_MESSAGE_MODE",
            expected    = "an instance of a class derived from ModeBase",
            problem     = "value is not a valid output mode",
            how_to_fix  = (
                "Use one of the available modes: PRETTY, SIMPLE, ONELINE, LOG.",
                "A custom mode must inherit from ModeBase and implement _full_outcome().",
            ),
        )


_DESIGN_NOTES = """
# validate_message_mode

## Purpose
Validates the value of `DEFAULT_MESSAGE_MODE` in `SimpleExceptionSettings`.
Accepts an instance of any class derived from `ModeBase` — rejects anything else.
"""