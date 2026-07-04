from .print_context import print_context
from .print_problem import print_problem

__all__ = [
    "print_context",
    "print_problem",
]


_DESIGN_NOTES = """
# Exception Multiline Info Printers Sub-Package

## Purpose
Contains structural printing block utilities responsible for formatting and rendering high-density, 
potentially multi-line exception metadata states such as Problems and Context logs.

## Exported Registry

| Component         | Type     | Description                                                                       |
| :---------------- | :------- | :-------------------------------------------------------------------------------- |
| `print_problem`   | Function | Formats and tracks arrays or individual strings mapping the core failure problem. |
| `print_context`   | Function | Serializes state or auxiliary metadata associated with the current failure.       |
"""