from .SimpleExceptionInternalError import SimpleExceptionInternalError
from .SimpleExceptionModeError import SimpleExceptionModeError
from .SimpleExceptionSettingsError import SimpleExceptionSettingsError


_DESIGN_NOTES = """
# core/_internal_exceptions

## Contents
Infrastructure for internal library errors. These exceptions are used to report 
misconfigurations, mode failures, or internal logic errors within the 
`simplibs-exception` ecosystem itself.

| Name                           | Description                                              |
|--------------------------------|----------------------------------------------------------|
| `SimpleExceptionInternalError` | Base class for all internal exceptions                   |
| `SimpleExceptionModeError`     | Error related to output modes (PRETTY, LOG, etc.)        |
| `SimpleExceptionSettingsError` | Error related to `SimpleExceptionSettings` validation    |

## Isolation Strategy
These classes are strictly separated from the main `SimpleException` logic to 
prevent circular dependencies. They inherit directly from `SimpleExceptionData` 
and use a hardcoded `PRETTY` mode with `validate=False` to ensure they can 
always render their message, even if the global settings are corrupted.

## Catching Internal Errors
All internal errors can be caught using the base class:
```python
try:
    # Some library-related operation
    SimpleExceptionSettings.DEFAULT_GET_LOCATION = "invalid"
except SimpleExceptionInternalError as e:
    print(f"Internal library problem: {e}")
"""