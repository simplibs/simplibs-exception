from .bool_or_exception import bool_or_exception
from .raise_location_offset import raise_location_offset
from .raise_with_location_offset import raise_with_location_offset

__all__ = [
    "bool_or_exception",
    "raise_location_offset",
    "raise_with_location_offset",
]


_DESIGN_NOTES = """
# Developer Tools Sub-Package Entry Point

## Purpose
This package acts as an operational utility suite built upon the `SimpleException` core ecosystem. 
It consolidates advanced, non-intrusive functional helpers designed to minimize development boilerplate, 
optimize validation flow controls, and manage call-stack frame calibration.

## Exported Registry

| Component                    | Type      | Description                                                                             |
| :--------------------------- | :-------- | :-------------------------------------------------------------------------------------- |
| `bool_or_exception`          | Function  | Intercepts validation gates to return `False` or trigger a fully typed error instance. |
| `raise_with_location_offset` | Function  | Low-level imperative utility providing explicit trace-shifting mechanics for objects.  |
| `raise_location_offset`      | Decorator | High-level declarative macro automating runtime caller-site trace shifts on functions. |

## Architectural Responsibility
The `tools` sub-package is strictly focused on improving Developer Experience (DX). Every component 
leverages runtime structural duck-typing boundaries where appropriate. This guarantees complete 
decoupling from concrete top-level exceptions during boot phases, preventing initialization cross-locks 
while delivering specialized telemetry trace mutations.

## Design Non-Intrusiveness
All facilities housed within this namespace are completely optional. They exist to enhance architectural 
velocity (especially inside downstream framework decorator stacks or gatekeepers), while the core 
`SimpleException` engine remains fully functional and autonomous without them.
"""