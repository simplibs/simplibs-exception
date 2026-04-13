import json
# Inners
from .ToDict import ToDictMixin


class ToJsonMixin:
    """Mixin for serialising public instance attributes into a JSON string."""

    def to_json(self: ToDictMixin) -> str:
        """
        Returns the public instance attributes as a JSON string — UNSET values are omitted.

        Returns:
            A JSON string of the public instance attributes.
        """
        return json.dumps(self.to_dict(), default=str)


_DESIGN_NOTES = """
# ToJsonMixin

## Purpose
Serialises the public attributes of an instance into a JSON string — for
transport, logging, or storing exception state.

## Dependency
Requires `ToDictMixin` — calls `self.to_dict()` to obtain the data.
The connection is ensured by the protocol defined at the `SimpleException` level.

## Notes
- `default=str` ensures that values which are not directly JSON-serialisable
  (such as `type[Exception]`) are converted to a string instead of raising
  an error.
- Includes only public attributes — the same rule as `ToDictMixin`.
- A `to_debug_json()` method built on top of `to_debug_dict()` can be added
  for debugging including computed values — following the same pattern as the
  dict variants.
"""