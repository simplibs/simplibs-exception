# Inners
from .SimpleExceptionSettingsError import SimpleExceptionSettingsError


def validate_location_blacklist(value):
    """Verifies that the value is a tuple containing only strings."""

    # 1. Verify that the provided value is a tuple
    if not isinstance(value, tuple):
        raise SimpleExceptionSettingsError(
            value       = value,
            value_label = "DEFAULT_LOCATION_BLACKLIST",
            expected    = "tuple[str, ...] — a tuple of strings with file name patterns",
            problem     = "value is not a tuple",
            how_to_fix  = (
                "Wrap the value in a tuple: ('filename.py',)",
                "To set an empty blacklist use an empty tuple: ()",
            ),
        )

    # 2. Verify the items inside the tuple
    bad_items = [i for i in value if not isinstance(i, str)]
    if bad_items:
        raise SimpleExceptionSettingsError(
            value       = bad_items,
            value_label = "DEFAULT_LOCATION_BLACKLIST",
            expected    = "a tuple containing only strings",
            problem     = f"tuple contains {len(bad_items)} item(s) that are not strings",
            how_to_fix  = (
                "Check all items — each one must be a string (str).",
                "Each item defines a file name pattern that will be skipped during location resolution.",
            ),
        )


_DESIGN_NOTES = """
# validate_location_blacklist

## Purpose
Validates the value of `DEFAULT_LOCATION_BLACKLIST` in `SimpleExceptionSettings`.
Two checks are performed — the first fails fast, the second describes precisely
what is wrong.

## Checks
1. Verifies that the value is a `tuple` — if not, it is rejected immediately.
2. Iterates over all items and collects those that are not `str` — if any are
   found, they are all reported at once.
"""