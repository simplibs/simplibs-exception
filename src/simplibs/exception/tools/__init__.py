from .bool_or_exception import bool_or_exception
from .raise_with_location_offset import raise_with_location_offset
from .decorators import raise_location_offset


_DESIGN_NOTES = """
# tools

## Contents
Functional helpers and utilities that build upon the `SimpleException` 
ecosystem.

| Tool                         | Type        | Description                                      |
|------------------------------|-------------|--------------------------------------------------|
| `bool_or_exception`          | Function    | Conditional raising based on a boolean flag.     |
| `raise_with_location_offset` | Function    | Manual re-targeting of an exception's location.  |
| `raise_location_offset`      | Decorator   | Automated re-targeting of an exception's origin. |

## Responsibility
The `tools` package provides convenience methods that reduce boilerplate code. 
They leverage duck typing where possible to avoid rigid dependencies on the 
`SimpleException` class while still providing specialized behavior for it.

## Design Philosophy: Non-Intrusive
These tools are optional. They are designed to make the developer's life 
easier (especially when building libraries), but the core `SimpleException` 
functionality remains fully usable without them.
"""