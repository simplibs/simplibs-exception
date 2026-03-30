# Commons
from ....core import SimpleExceptionData
# Inners
from ._utils import check_children_class_attributes


class DunderInitSubclassMixin:
    """Mixin for validating subclasses at definition time."""

    def __init_subclass__(
        cls,
        **kwargs
    ) -> None:
        """
        Validates the subclass when it is defined — checks for typos and incorrect attribute types.

        Args:
            cls: The newly defined class (subclass).
        """
        super().__init_subclass__(**kwargs)
        check_children_class_attributes(SimpleExceptionData, cls)


_DESIGN_NOTES = """
# DunderInitSubclassMixin

## Purpose
Validates `SimpleException` subclasses at **definition time** — that is, at
import, not when an instance is created. Developer errors (typos, incorrect
attribute types) are surfaced immediately.

## Why at class definition time rather than at instantiation
`__init_subclass__` is called automatically by Python the moment the
interpreter processes the subclass definition. This means the developer
receives an error immediately on module import — not somewhere during
program execution where the root cause would be harder to trace.

## What is checked
Delegates to `check_children_class_attributes`, which verifies:
- The subclass contains no attributes not defined in `SimpleExceptionData`
  (likely typos)
- Attribute values match the types declared in `SimpleExceptionData`

## Why the logic lives in a separate function
`__init_subclass__` decides **when** to validate.
`check_children_class_attributes` decides **how** to validate.
Separation of concerns — the mixin remains a clean orchestrator that is
readable at a glance. The validation logic itself (~35 lines with two
branches and walrus operators) would clutter the method to the point where
the intent would no longer be obvious without reading the details.

## Notes
- `super().__init_subclass__(**kwargs)` must always be called first —
  this ensures correct MRO behaviour under multiple inheritance.
- The private implementation detail `check_children_class_attributes` lives
  in the `_utils` subdirectory alongside this mixin — it does not leave
  that scope.
- Errors are reported via `SimpleExceptionInternalError` — an internal
  library exception that signals a developer error, not a runtime error.
"""