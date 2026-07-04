from .CallerInfo import CallerInfoMixin


_DESIGN_NOTES = """
# _exception_mixins/properties

## Contents
Mixins that extend `SimpleException` with managed attributes (properties).

| Mixin             | Property      | Description                                               |
|-------------------|---------------|-----------------------------------------------------------|
| `CallerInfoMixin` | `caller_info` | Lazily-computed dictionary with call site information     |

## Responsibility
These mixins provide high-level access to computed data. By using properties 
instead of regular methods, we keep the exception API intuitive and 
attribute-like, while maintaining the benefits of lazy evaluation and caching.
"""