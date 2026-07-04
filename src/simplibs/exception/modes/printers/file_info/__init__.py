from .print_file_info import print_file_info
from .print_file_path import print_file_path

__all__ = [
    "print_file_info",
    "print_file_path",
]


_DESIGN_NOTES = """
# File Information Printers Sub-Package

## Purpose
Orchestrates string formatting utilities targeted at extracting, mapping, and serializing file 
origins, line counts, and caller-site module pathways found inside the telemetry trace layout.

## Exported Registry

| Component           | Type     | Description                                                              |
| :------------------ | :------- | :----------------------------------------------------------------------- |
| `print_file_info`   | Function | Formats the compact source location marker (`file.py:line`).             |
| `print_file_path`   | Function | Serializes the complete absolute or relative filesystem path.            |
"""