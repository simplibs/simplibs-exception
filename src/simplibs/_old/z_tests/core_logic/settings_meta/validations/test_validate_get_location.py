from typing import Any
# Outers
from ....core_logic.internal_exceptions import SimpleExceptionSettingsError


def validate_get_location(
    value: Any
) -> None:
    """Verifies that the value is an int or bool."""
    if not isinstance(value, (int, bool)):
        raise SimpleExceptionSettingsError(
            value=value,
            label="GET_LOCATION",
            expected="int or bool (e.g., True, False, 1, 2)",
            problem="value is neither a boolean nor an integer",
            how_to_fix=(
                "Pass True or False to enable or disable location reporting.",
                "Pass a positive int to set the stack depth traversal limit (e.g., 1, 2).",
            ),
        )


_DESIGN_NOTES = """
# validate_get_location

## Purpose
Validates the configuration state of the `GET_LOCATION` attribute within `SimpleExceptionSettings`.
Enforces that the tracing trigger configuration strictly adheres to valid primitive types.

## Type Constraints & Python Subclassing Nuance
The validator evaluates the payload against a type-tuple of `(int, bool)`. 
In Python's core type architecture, `bool` is inherently an explicit subclass of `int` (`isinstance(True, int)` 
evaluates to `True`). Because both integer depth offsets and boolean feature flags represent valid operational 
states for the stack frame location engine, a combined `isinstance` pass safely permits both variants while 
immediately blocking complex un-hashable types, strings, or custom objects.
"""