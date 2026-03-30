from typing import get_type_hints
from simplibs.sentinels import UNSET


class ToDictMixin:
    """Mixin for serialising public instance attributes into a dictionary."""

    def to_dict(self) -> dict:
        """
        Returns the public instance attributes as a dictionary — UNSET values are omitted.

        Returns:
            A dictionary of public attributes (without a leading underscore)
            and their current values.
        """
        # get_type_hints collects annotations from the current class and all its ancestors
        all_annotations = get_type_hints(self.__class__)

        return {
            name: getattr(self, name)
            for name in all_annotations
            if not name.startswith("_")
            and getattr(self, name) is not UNSET
        }


_DESIGN_NOTES = """
# ToDictMixin

## Purpose
Serialises the public attributes of an instance into a dictionary — for
reconstruction, transport, or comparison of exception state.

## Why get_type_hints instead of __annotations__
The standard approach via `self.__class__.__annotations__` returns only the
annotations defined directly on that class. If the user creates a subclass,
attributes inherited from parent classes would not be visible.
Using `get_type_hints(self.__class__)` correctly walks the entire inheritance
hierarchy (MRO) and returns a unified set of all available annotations.

## Attribute collection rule
Includes only attributes **without a leading underscore** — those that the
user can set as parameters or class-level attributes. Computed values
(with a leading underscore such as `_intercepted_exception`, `_get_location`)
are intentionally excluded. UNSET values are omitted — they represent
parameters that were not provided.

## Notes
- Collection is automatic based on class annotations — adding a new public
  attribute to `SimpleExceptionData` is automatically reflected here as well.
- For debugging including computed values, use `ToDebugDictMixin`.
"""