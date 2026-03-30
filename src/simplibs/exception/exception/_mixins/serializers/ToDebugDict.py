from typing import get_type_hints
from simplibs.sentinels import UNSET
# Inners
from .ToDict import ToDictMixin


class ToDebugDictMixin:
    """Mixin for serialising all instance attributes into a dictionary for debugging."""

    def to_debug_dict(self: ToDictMixin) -> dict:
        """
        Returns all instance attributes as a dictionary — including computed values.
        UNSET values are omitted.

        Returns:
            A dictionary of all attributes (public and private) with their current values.
        """
        all_hints = get_type_hints(self.__class__)

        # Private attributes defined in annotations (e.g. _get_location, _oneline)
        annotated_private = {
            name: getattr(self, name)
            for name in all_hints
            if name.startswith("_")
               and not name.startswith("__")
               and getattr(self, name, UNSET) is not UNSET
        }

        # Private attributes assigned in __init__ without an annotation (e.g. _rendered_message)
        unannotated_private = {
            name: value
            for name, value in self.__dict__.items()
            if name.startswith("_")
               and not name.startswith("__")
               and name not in all_hints
               and value is not UNSET
        }

        return {**self.to_dict(), **annotated_private, **unannotated_private}


_DESIGN_NOTES = """
# ToDebugDictMixin

## Purpose
Extends `ToDictMixin` with computed values — for logging, debugging, and
detailed introspection of exception state. Provides a complete view of the
entire instance state, including values that are produced at runtime in
`__init__`.

## Why get_type_hints
As with `ToDictMixin`, `get_type_hints(self.__class__)` is used here to
ensure full inheritance support. Without this call, the mixin would not see
private attributes defined in parent classes (e.g. those declared in
`SimpleExceptionData`) when called on a subclass instance.

## Attribute collection rule
The resulting dictionary is assembled from three sources:

1. **Public attributes** — via `to_dict()`, annotated only, without a leading
   underscore, UNSET values omitted.
2. **Private annotated attributes** — attributes with a single leading
   underscore defined in class annotations (e.g. `_get_location`, `_oneline`,
   `_skip_locations` from `SimpleExceptionData`). Collected via `get_type_hints`.
3. **Private unannotated attributes** — attributes with a single leading
   underscore assigned in `__init__` without an annotation (e.g.
   `_rendered_message`). Collected via `self.__dict__`.

Attributes with a double leading underscore (`__`) are intentionally excluded
— these are Python-internal attributes (name mangling) that do not belong in
debug output. UNSET values are omitted from all three sources.

## Why two sources for private attributes
`get_type_hints` returns only annotated attributes — attributes assigned in
`__init__` without an annotation (such as `_rendered_message`) would be
missing from the output without `self.__dict__`. Combining both sources
ensures that the debug output is truly complete.

## Dependency
Requires `ToDictMixin` — calls `self.to_dict()` as the base of the dictionary.
The connection is ensured by the protocol defined at the `SimpleException` level.

## Notes
- Adding a new private attribute to `SimpleExceptionData` (annotated) or to
  `SimpleException.__init__` (unannotated) is automatically reflected here.
- The output is intended exclusively for debugging and logging — not for
  transport or reconstruction of the exception.
"""