from .extract_caller_info import extract_caller_info
from .bool_or_exception import bool_or_exception


_DESIGN_NOTES = """
# utils

## Contents
Shared utilities for the library — two self-contained helpers,
each with a different character and responsibility.

| Name                  | Description                                                   |
|-----------------------|---------------------------------------------------------------|
| `extract_caller_info` | Diagnostic function for determining the call site in the stack |
| `bool_or_exception`   | Shortcut for conditional exception raising                    |

## Notes
- `extract_caller_info` is independent of the rest of the library —
  it has no dependencies and can be used anywhere.
- `bool_or_exception` depends on `SimpleException`; the lazy import
  inside the function prevents a circular dependency.
"""