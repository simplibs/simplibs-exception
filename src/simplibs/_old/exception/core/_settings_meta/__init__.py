from .SimpleExceptionSettingsMeta import SimpleExceptionSettingsMeta


_DESIGN_NOTES = """
# settings/_meta

## Contents
The infrastructure for `SimpleExceptionSettings`. This package contains the 
metaclass and its validation logic, kept separate to keep the main settings 
class clean.

| Name                           | Description                                              |
|--------------------------------|----------------------------------------------------------|
| `SimpleExceptionSettingsMeta`  | Metaclass — validates writes via `__setattr__`           |

## Responsibility
This module acts as the "gatekeeper" for the library configuration. 
The `SimpleExceptionSettingsMeta` class uses validators from the sub-package 
`validations` to ensure that any change to global settings is safe and correct.

The individual validators are not exported here because they are considered 
private implementation details of the Metaclass.
"""