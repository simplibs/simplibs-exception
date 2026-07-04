from .dividers import DOT_PREFIX, DOUBLE_LINE, EMPTY_PREFIX, SINGLE_LINE
from .exception_info_multiline import print_context, print_problem
from .exception_info_oneline import print_expected, print_message, print_value_with_type
from .file_info import print_file_info, print_file_path
from .hepl_info import print_how_to_fix, print_intercepted_exception
from .intro import print_intro

__all__ = [
    # Dividers
    "DOT_PREFIX",
    "DOUBLE_LINE",
    "EMPTY_PREFIX",
    "SINGLE_LINE",
    # Multiline
    "print_context",
    "print_problem",
    # Oneline
    "print_expected",
    "print_message",
    "print_value_with_type",
    # File Info
    "print_file_info",
    "print_file_path",
    # Help Info
    "print_how_to_fix",
    "print_intercepted_exception",
    # Intro
    "print_intro",
]


_DESIGN_NOTES = """
# Master Printers Aggregation Gateway

## Purpose
This package serves as a centralized internal junction box. It aggregates all decoupled, leaf-level 
printing micro-utilities and layout components, re-exporting them in a flat layout for easy 
consumption by the higher-level concrete Render Mode Engines.

## Consolidated Exported Registry

| Category        | Components                                            | Description                                              |
| :-------------- | :---------------------------------------------------- | :------------------------------------------------------- |
| **Dividers**    | `DOUBLE_LINE`, `SINGLE_LINE`, `DOT_PREFIX`, `EMPTY_PREFIX` | Structural dividers and indentation tokens.              |
| **Multiline**   | `print_problem`, `print_context`                      | Formatting utilities for multiline exception metadata.   |
| **Oneline**     | `print_message`, `print_expected`, `print_value_with_type` | Compact single-line formatting helpers.                  |
| **File Info**   | `print_file_info`, `print_file_path`                  | Source location and filesystem path formatting.          |
| **Help Info**   | `print_how_to_fix`, `print_intercepted_exception`     | User guidance and chained exception rendering.           |
| **Intro**       | `print_intro`                                         | Leading exception header generation.                     |
"""