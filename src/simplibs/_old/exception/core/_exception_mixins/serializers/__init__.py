from .ToDict import ToDictMixin
from .ToDebugDict import ToDebugDictMixin
from .ToJson import ToJsonMixin


_DESIGN_NOTES = """
# _exception_mixins/serializers

## Contents
Mixins providing various formats for exporting exception data. These methods 
are useful for logging, API responses, or cross-service error propagation.

| Mixin              | Method            | Scope                                               |
|--------------------|-------------------|-----------------------------------------------------|
| `ToDictMixin`      | `to_dict()`       | Public attributes only (clean data)                 |
| `ToDebugDictMixin` | `to_debug_dict()` | Public + private + computed attributes (full state) |
| `ToJsonMixin`      | `to_json()`       | Public attributes as a JSON string                  |

## Design Philosophy: Introspection
By using `get_type_hints`, these mixins are "future-proof". Any new attribute 
added to `SimpleExceptionData` is automatically included in the exports 
without needing to modify the serialization logic.

## Formatting Rules
- **UNSET Omission:** Attributes that haven't been set (holding the `UNSET` 
  sentinel) are excluded from the output to keep it clean.
- **JSON Safety:** `to_json` uses a string fallback for non-serializable 
  objects, ensuring that the export process itself never raises an exception.

## Integration
These mixins are mixed into the main `SimpleException` class, providing 
users with a simple way to convert an exception instance into a 
transportable format.
"""