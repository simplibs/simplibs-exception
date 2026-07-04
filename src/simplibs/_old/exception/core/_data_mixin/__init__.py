from .properties import CallerInfoMixin


_DESIGN_NOTES = """
# _data_mixin

## Purpose
A specialized layer of mixins designed specifically for the data structures 
of the ecosystem (e.g., `SimpleExceptionData`). 

## Key Characteristic: Foundation
Unlike `_exception_mixins`, which focus on the full `SimpleException` logic, 
`_data_mixin` provides essential capabilities that must be available to 
ALL exceptions, including internal library errors.

## Contents
| Mixin              | Responsibility                                             |
|--------------------|------------------------------------------------------------|
| `CallerInfoMixin`  | Provides lazy, cached access to the exception's call site. |

## Why this separation?
By attaching `CallerInfoMixin` to `SimpleExceptionData` at this level, we 
ensure that even `SimpleExceptionInternalError` is location-aware. This 
avoids code duplication and ensures that renderers can always rely on 
`data.caller_info` being available.
"""