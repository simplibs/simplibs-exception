from dataclasses import dataclass
# Commons
from ....core import SimpleExceptionInternalError

@dataclass
class SimpleExceptionModeError(SimpleExceptionInternalError):
    error_name: str = "MODE ERROR"


_DESIGN_NOTES = """
# SimpleExceptionModeError

## Purpose
A grouped exception for errors related to `SimpleException` output modes.
Inherits from `SimpleExceptionInternalError` — it is therefore completely
isolated from `SimpleException` logic and from the modes themselves.

## Isolation from core logic
Internal library exceptions cannot use `SimpleException` — it would create
a circular import. `SimpleExceptionModeError` inherits its isolation from
`SimpleExceptionInternalError`, which builds directly on `SimpleExceptionData`
and `Exception`.

## Group
Can be caught as a common type for all mode-related errors:
```python
except SimpleExceptionModeError:
    # invalid data passed to a mode, or another error during output processing
```
"""