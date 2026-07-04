from .SimpleExceptionData import SimpleExceptionData
from .SimpleExceptionSettings import SimpleExceptionSettings


_DESIGN_NOTES = """
# core

## Purpose
The foundational layer of the SimpleException system. This package contains 
the base data structures, global configuration, and internal building blocks 
(mixins) that define the exception's behavior.

## Contents
This entry point exposes the two most important public components:

| Class                       | Responsibility                                           |
|-----------------------------|----------------------------------------------------------|
| `SimpleExceptionData`       | Defines the data structure and default attribute values. |
| `SimpleExceptionSettings`   | Manages global library-wide configuration and defaults.  |

## Sub-packages (Internal)
The following internal directories are managed within this layer:
- `_exception_mixins`: Modular building blocks for the main exception class.
- `_internal_exceptions`: Guard exceptions used during the boot/validation phase.
- `_settings_meta`: Metadata and logic for the settings management.

## Integration
By exposing only `SimpleExceptionData` and `SimpleExceptionSettings`, we provide 
a clean API for the rest of the library while keeping the complex mixin 
infrastructure hidden as an internal implementation detail.
"""