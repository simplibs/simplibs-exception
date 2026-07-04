# Outers
from ..._internal_exceptions import SimpleExceptionSettingsError


def validate_value_truncation_length(value):
    """
    Verifies that the value is a positive integer.

    Args:
        value: The value to validate.

    Raises:
        SimpleExceptionSettingsError: If value is not a positive int.
    """
    # 1. Verify that the value is an integer (and not a boolean)
    if not isinstance(value, int) or isinstance(value, bool):
        raise SimpleExceptionSettingsError(
            value=value,
            value_label="DEFAULT_VALUE_TRUNCATION_LENGTH",
            expected="a positive integer (e.g. 50, 100, 200)",
            problem="value is not an integer",
            how_to_fix=(
                "Pass an integer value — e.g. 100, 200, 500.",
                "This value controls how many characters to show before truncating large values.",
            ),
        )

    # 2. Verify that the number is positive
    if value <= 0:
        raise SimpleExceptionSettingsError(
            value=value,
            value_label="DEFAULT_VALUE_TRUNCATION_LENGTH",
            expected="a positive integer greater than 0",
            problem="value is zero or negative",
            how_to_fix=(
                "Pass a value greater than 0 — e.g. 50, 100.",
                "Recommended: 50-200 depending on your terminal width and preference.",
            ),
        )


_DESIGN_NOTES = """
# validate_value_truncation_length

## Purpose
Validates the value of `DEFAULT_VALUE_TRUNCATION_LENGTH` in `SimpleExceptionSettings`.
Ensures that the limit for text truncation is a valid positive integer.

## Checks
1. **Type check** — verifies that the value is an `int`. Specifically excludes 
   `bool`, because in Python `isinstance(True, int)` is true, which would 
   otherwise bypass this check.
2. **Value check** — verifies that the integer is greater than zero. A zero or 
   negative length wouldn't make sense for displaying value representation.

## Design Decision
The limit is applied to the result of `repr(value)`. By keeping this value 
relatively low (default 100), we ensure that even complex data structures 
remain readable and do not "explode" the terminal output, while still 
providing enough context to identify the data.
"""