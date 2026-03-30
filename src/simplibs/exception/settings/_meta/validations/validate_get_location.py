# Inners
from .SimpleExceptionSettingsError import SimpleExceptionSettingsError


def validate_get_location(value):
    """Verifies that the value is an int or bool."""
    if not isinstance(value, (int, bool)):
        raise SimpleExceptionSettingsError(
            value       = value,
            value_label = "DEFAULT_GET_LOCATION",
            expected    = "int or bool (e.g. True, False, 1, 2)",
            problem     = "value is neither an int nor a bool",
            how_to_fix  = (
                "Pass True or False to enable or disable location reporting.",
                "Pass an int to set the stack depth (e.g. 1, 2).",
            ),
        )


_DESIGN_NOTES = """
# validate_get_location

## Purpose
Validates the value of `DEFAULT_GET_LOCATION` in `SimpleExceptionSettings`.
Accepts `int` or `bool` — rejects anything else.
"""