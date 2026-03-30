from .SimpleExceptionSettingsMeta import SimpleExceptionSettingsMeta
from .validations import SimpleExceptionSettingsError


_DESIGN_NOTES = """
# settings/_meta

## Contents
The metaclass for validating attribute assignments on `SimpleExceptionSettings`
and the grouped exception for settings-related errors.

| Name                           | Description                                              |
|--------------------------------|----------------------------------------------------------|
| `SimpleExceptionSettingsMeta`  | Metaclass — validates writes via `__setattr__`           |
| `SimpleExceptionSettingsError` | Grouped exception propagated for external use            |
"""