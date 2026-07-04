from typing import Any
# Outers
from ...._core_logic.internal_exceptions import SimpleExceptionSettingsError
from ....modes import ModeBase


def validate_message_mode(value: Any) -> None:
    """Verifies that the value is an instance of a class derived from ModeBase."""
    if not isinstance(value, ModeBase):
        raise SimpleExceptionSettingsError(
            value=value,
            label="MESSAGE_MODE",
            expected="an instance of a class derived from ModeBase (e.g., PRETTY, SIMPLE, ONELINE, LOG)",
            problem="value is not a valid framework output mode configuration",
            how_to_fix=(
                "Use one of the pre-configured built-in singletons: PRETTY, SIMPLE, ONELINE, LOG.",
                "If building a custom formatting engine, ensure it inherits strictly from ModeBase.",
            ),
        )


_DESIGN_NOTES = """
# validate_message_mode

## Purpose
Validates the configuration state of the `MESSAGE_MODE` attribute within `SimpleExceptionSettings`.
Guarantees that the presentation layout engine is bound to an authorized formatting class.

## Architectural Validation Strategy
The validator enforces explicit inheritance constraint checks via `isinstance(value, ModeBase)`. 
While static structural protocols handle type-hinting signatures for public interfaces, runtime 
execution requires a solid object ancestry verification because `ModeBase` encapsulates shared layout 
contracts. Importing `ModeBase` here maintains a strict top-down dependency flow, naturally remaining 
immune to circular import deadlocks.
"""