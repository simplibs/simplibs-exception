from .ToDict import ToDictMixin
from .ToDebugDict import ToDebugDictMixin
from .ToJson import ToJsonMixin


_DESIGN_NOTES = """
# exception/_mixins/serializers

## Contents
Mixins for serialising the state of `SimpleException` into various formats.

| Name              | Method          | Description                                           |
|-------------------|-----------------|-------------------------------------------------------|
| `ToDictMixin`     | `to_dict`       | Public attributes as a dictionary                     |
| `ToDebugDictMixin`| `to_debug_dict` | Public and computed attributes as a dictionary        |
| `ToJsonMixin`     | `to_json`       | Public attributes as a JSON string                    |
"""