from dataclasses import dataclass
# Commons
from ....core import SimpleExceptionInternalError

@dataclass
class SimpleExceptionSettingsError(SimpleExceptionInternalError):
    error_name: str = "SETTINGS ERROR"


_DESIGN_NOTES = """
# SimpleExceptionSettingsError

## Purpose
A grouped exception for errors related to `SimpleExceptionSettings` configuration.
Inherits from `SimpleExceptionInternalError` — it is therefore completely
isolated from `SimpleException` and `SimpleExceptionSettings` logic.

## Isolation from core logic
Internal library exceptions cannot use `SimpleException` — it would create
a circular import. `SimpleExceptionInternalError` therefore builds directly
on `SimpleExceptionData` and `Exception`, with no dependency on the rest of
the library. `SimpleExceptionSettingsError` inherits this isolation.

## Group
Can be caught as a common type for all settings-related errors:
```python
except SimpleExceptionSettingsError:
    # invalid value or unknown attribute in SimpleExceptionSettings
```
"""