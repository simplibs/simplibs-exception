from typing import Any
# Outers
from ...._core_logic.internal_exceptions import SimpleExceptionSettingsError


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

    if type(value) is int and value < 0:
        raise SimpleExceptionSettingsError(
            value=value,
            label="GET_LOCATION",
            expected="a non-negative integer (>= 0) or bool",
            problem="integer depth offset cannot be negative",
            how_to_fix=(
                "Pass a positive integer or 0 to define a valid stack traversal depth.",
                "Negative numbers are not supported by the Python frame inspection engine."
            )
        )


_DESIGN_NOTES = """
# validate_get_location

## Purpose
Validates the configuration state of the `GET_LOCATION` attribute within `SimpleExceptionSettings`.
Enforces that the tracing trigger configuration strictly adheres to valid primitive types and values.

## Type Constraints & Python Subclassing Nuance
The validator evaluates the payload against a type-tuple of `(int, bool)`. 
In Python's core type architecture, `bool` is inherently an explicit subclass of `int` (`isinstance(True, int)` 
evaluates to `True`). Because both integer depth offsets and boolean feature flags represent valid operational 
states for the stack frame location engine, a combined `isinstance` pass safely permits both variants while 
immediately blocking complex un-hashable types, strings, or custom objects.

## Value Boundary Constraints & Negative Offsets
While the type check passes both `int` and `bool`, a strict secondary value gate filters out negative integers.
The underlying stack-scanning subsystem relies on Python's frame inspection mechanics (`sys._getframe(depth)`). 
Python interprets `depth` as a forward-stepping count from the current execution anchor (where `0` is the immediate 
local space, `1` is the caller, etc.). Passing a negative integer to the native interpreter engine triggers a terminal 
`ValueError: frame index must not be negative`. To prevent the telemetry framework from crashing internally during 
exception formatting, negative depth configurations are rejected at the gate.
"""