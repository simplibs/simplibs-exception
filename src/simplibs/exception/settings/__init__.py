from .SimpleExceptionSettings import SimpleExceptionSettings
from ._meta.validations import SimpleExceptionSettingsError


_DESIGN_NOTES = """
# settings

## Contents
The central configuration of the library and the exception for settings-related errors.

| Name                           | Description                                                    |
|--------------------------------|----------------------------------------------------------------|
| `SimpleExceptionSettings`      | Central configuration — the single source of truth for the ecosystem |
| `SimpleExceptionSettingsError` | Exception for catching errors when changing settings           |

## Usage
```python
from simple_exception.settings import SimpleExceptionSettings

SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = LOG
SimpleExceptionSettings.reset()
```
"""