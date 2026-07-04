from .print_intro import print_intro

__all__ = [
    "print_intro",
]


_DESIGN_NOTES = """
# Introduction Printers Sub-Package

## Purpose
Isolates layout generators that output the initial header segment banner of the diagnostic block, 
responsible for parsing the exception class name context.

## Exported Registry

| Component     | Type     | Description                                                  |
| :------------ | :------- | :----------------------------------------------------------- |
| `print_intro` | Function | Formats and outputs the leading error header or banner.      |
"""