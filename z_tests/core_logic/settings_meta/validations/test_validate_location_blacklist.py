from typing import Any
# Outers
from ....core_logic.internal_exceptions import SimpleExceptionSettingsError


def validate_location_blacklist(
    value: Any
) -> None:
    """Verifies that the value is a tuple containing only strings."""
    # 1. Verify that the provided value is a tuple
    if not isinstance(value, tuple):
        raise SimpleExceptionSettingsError(
            value=value,
            label="LOCATION_BLACKLIST",
            expected="tuple[str, ...] — a tuple of strings containing filename patterns",
            problem="value is not a tuple",
            how_to_fix=(
                "Wrap the value in a tuple: ('filename.py',)",
                "To set an empty blacklist use an empty tuple: ()",
            ),
        )

    # 2. Verify the items inside the tuple
    bad_items = [i for i in value if not isinstance(i, str)]
    if bad_items:
        raise SimpleExceptionSettingsError(
            value=bad_items,
            label="LOCATION_BLACKLIST",
            expected="a tuple containing only string elements",
            problem=f"tuple contains invalid non-string elements (found {len(bad_items)} invalid item(s))",
            how_to_fix=(
                "Check all items — each one must be a string (str).",
                "Each item defines a file name pattern that will be skipped during location resolution.",
            ),
        )


_DESIGN_NOTES = """
# validate_location_blacklist

## Purpose
Validates the configuration state of the `LOCATION_BLACKLIST` attribute within `SimpleExceptionSettings`.
It implements a multi-stage validation sequence to prevent structural type pollution inside the trace engine.

## Structural Verification Lifecycle
1. **Container Check**: Asserts that the incoming payload is a strict Python `tuple`. If it is any other 
   iterable (like a list or set), it fails fast to enforce an immutable boundary.
2. **Element Deep-Scan**: Iterates through the collection, aggregating all non-string elements into a 
   `bad_items` matrix. If the collection is polluted, it reports every single offending element simultaneously, 
   providing immediate corrective feedback.
"""