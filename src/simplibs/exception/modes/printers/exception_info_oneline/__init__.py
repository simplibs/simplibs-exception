from .print_expected import print_expected
from .print_message import print_message
from .print_value_with_type import print_value_with_type

__all__ = [
    "print_expected",
    "print_message",
    "print_value_with_type",
]


_DESIGN_NOTES = """
# Exception Oneline Info Printers Sub-Package

## Purpose
Manages low-level printing macros tailored for immediate, single-row string formatting of primary 
exception fields, ensuring defensive type mapping and truncation bounds are fully respected.

## Exported Registry

| Component               | Type     | Description                                                                    |
| :---------------------- | :------- | :----------------------------------------------------------------------------- |
| `print_message`         | Function | Serializes the primary root error message.                                     |
| `print_expected`        | Function | Formats the definition block describing valid type or state constraints.       |
| `print_value_with_type` | Function | Formats the input value together with its native Python type annotation.        |
"""