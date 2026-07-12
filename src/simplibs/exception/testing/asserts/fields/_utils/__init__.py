from .compare_strings import compare_strings
from ._normalize_value import _normalize_value

_DESIGN_NOTES = """
# Asserts Fields Sub-Engine Utilities Registry

## Purpose
Provides isolated, high-performance utility blades required for the internal operation 
of the fields assertion engine. These components handle data normalization and 
textual inspection logic, ensuring the public assertion API remains clean and focused.

## Internal Components Registry

| Component          | Type                 | Description                                                 |
| :----------------- | :------------------- | :---------------------------------------------------------- |
| `compare_strings`  | Inspection Engine    | Multi-modal textual evaluation engine (Exact/Prefix/Fuzzy). |
| `_normalize_value`  | Sanitization Utility | Data flattening and type-coercion gate for textual inputs.   |

## Access Restriction
These utilities are intended strictly for internal usage within `simplibs.exception.testing.asserts.fields`. 
They are not part of the public API surface; therefore, they are not exported via `__all__`.
"""