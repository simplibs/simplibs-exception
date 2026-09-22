from .StateError import StateError
from .InitializationError import InitializationError
from .ConfigurationError import ConfigurationError


_DESIGN_NOTES = """
# State Errors Sub-Package

## Purpose
Groups every exception concerned with "an object or system is not in the state a given operation
requires": the general `StateError` and its more specific descendants.

## Registry

| Component              | Type  | Description                                                                 |
| :------------------------ | :---- | :---------------------------------------------------------------------------- |
| `StateError`           | Class | An object or system is not in the state a given operation requires.         |
| `InitializationError`  | Class | An object or system was used before it was properly initialized.            |
| `ConfigurationError`   | Class | Required configuration is missing or invalid.                               |
"""