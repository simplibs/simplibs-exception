from typing import Any
# Outers
from ...._core_logic.internal_exceptions import SimpleExceptionSettingsError


def validate_value_truncation_length(value: Any) -> None:
    """Verifies that the value is a positive integer.

    Raises:
        SimpleExceptionSettingsError: If value is not a positive int.
    """
    # 1. Verify that the value is an integer (and strictly not a boolean)
    if not isinstance(value, int) or isinstance(value, bool):
        raise SimpleExceptionSettingsError(
            value=value,
            label="VALUE_TRUNCATION_LENGTH",
            expected="a positive integer (e.g., 50, 100, 200)",
            problem="value is not an integer",
            how_to_fix=(
                "Pass an integer value — e.g., 100, 200, 500.",
                "This value controls how many characters to show before truncating large values.",
            ),
        )

    # 2. Verify that the number is positive
    if value <= 0:
        raise SimpleExceptionSettingsError(
            value=value,
            label="VALUE_TRUNCATION_LENGTH",
            expected="a positive integer greater than 0",
            problem="value is zero or negative",
            how_to_fix=(
                "Pass a value greater than 0 — e.g., 50, 100.",
                "Recommended: 50-200 depending on your terminal width and layout preference.",
            ),
        )


_DESIGN_NOTES = """
# validate_value_truncation_length

## Purpose
Validates the configuration state of the `VALUE_TRUNCATION_LENGTH` attribute within `SimpleExceptionSettings`.
Ensures that the boundary string representation truncation gate receives valid positive metrics.

## Structural Verification Lifecycle
1. **Defensive Type Gate**: Asserts that the incoming payload is an `int`. Since Python's object matrix 
   treats `bool` as a structural subclass of `int`, an explicit `isinstance(value, bool)` rejection check is 
   evaluated to prevent booleand values (`True`/`False`) from erroneously satisfying the boundary type constraint.
2. **Value Constraint Evaluation**: Blocks integers that are zero or negative, enforcing a boundary ruleset 
   where the maximum character buffer slice must always remain `> 0`.
"""