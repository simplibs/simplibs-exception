from .extract_caller_info import extract_caller_info
from .with_location_offset import with_location_offset


_DESIGN_NOTES = """
# Telemetry Stack Tracing Sub-Package

## Purpose
Low-level computational subsystem interacting with the interpreter's frame vectors to discover, filter, 
and return caller-site filepath locations and line indicators while skipping active blacklists.

## Internal Components Registry

| Component               | Type     | Description                                                                         |
| :---------------------- | :------- | :---------------------------------------------------------------------------------- |
| `extract_caller_info`   | Function | Resolves caller information by traversing stack frames and applying skip rules.     |
| `with_location_offset`  | Function | Adjusts the internally resolved caller location by applying an offset.              |
"""