# Commons
from ....core import SimpleExceptionData
# Inners
from .SimpleExceptionModeError import SimpleExceptionModeError


def validate_has_simple_exception_data(data: object) -> None:
    """Verifies that the object is an instance of SimpleExceptionData or a subclass."""
    if not isinstance(data, SimpleExceptionData):
        raise SimpleExceptionModeError(
            value       = data,
            value_label = "data",
            expected    = "an instance of SimpleExceptionData or a subclass",
            problem     = "the provided object does not have the SimpleExceptionData structure",
            how_to_fix  = (
                "Pass an instance of SimpleExceptionData or a class that inherits from it.",
                "For internal calls use validate=False — this check will be skipped.",
            ),
        )


_DESIGN_NOTES = """
# validate_has_simple_exception_data

## Purpose
Verifies that the provided object is an instance of `SimpleExceptionData`
or a subclass — meaning it has the structure that output modes expect.

## When it is called
Exclusively from `ModeBase.render_message()` when `validate=True`.
Internal library calls always pass `validate=False` — this function
therefore never executes during normal library use.

## Why it exists
A safeguard for cases where the user calls a mode directly with custom data —
for example when developing a custom mode or during testing. Without this
validation, a structural error in the data would produce a difficult-to-read
`AttributeError` deep inside the mode.

## Notes
- Uses `isinstance` — verifies actual inheritance, not just attribute presence.
- Raises `SimpleExceptionModeError` — an exception isolated from the
  core library logic.
"""