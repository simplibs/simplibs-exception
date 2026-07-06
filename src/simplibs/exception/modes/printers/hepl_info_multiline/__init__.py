from .print_how_to_fix import print_how_to_fix
from .print_intercepted_exception import print_intercepted_exception

__all__ = [
    "print_how_to_fix",
    "print_intercepted_exception",
]


_DESIGN_NOTES = """
# Help Information Printers Sub-Package

## Purpose
Manages layout blocks dealing with actionable developer remedies and deep serialization 
of foreign, intercepted underlying standard python exceptions chained to the core instance.

## Exported Registry

| Component                     | Type     | Description                                                                    |
| :---------------------------- | :------- | :----------------------------------------------------------------------------- |
| `print_how_to_fix`            | Function | Serializes actionable troubleshooting steps and user guidance.                 |
| `print_intercepted_exception` | Function | Formats and aligns intercepted or chained exceptions for display.              |
"""