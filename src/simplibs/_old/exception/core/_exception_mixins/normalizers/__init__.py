from .NormalizeParam import NormalizeParamMixin
from .ProcessExceptionParam import ProcessExceptionParamMixin
from .ProcessGetLocationParam import ProcessGetLocationParamMixin
from .ProcessHowToFixParam import ProcessHowToFixParamMixin
from .ProcessSkipLocationsParam import ProcessSkipLocationsParamMixin


_DESIGN_NOTES = """
# _exception_mixins/normalizers

## Contents
A group of mixins responsible for sanitizing and normalizing input parameters 
passed to the `SimpleException` constructor.

| Mixin                            | Responsibility                                           |
|----------------------------------|----------------------------------------------------------|
| `NormalizeParamMixin`            | Basic type-checking and fallback to class defaults       |
| `ProcessExceptionParamMixin`     | Handling exception classes vs. instances                 |
| `ProcessGetLocationParamMixin`   | Resolving location depth against global settings         |
| `ProcessHowToFixParamMixin`      | Formatting strings or lists into a consistent tuple      |
| `ProcessSkipLocationsParamMixin` | Merging local skip patterns with the global blacklist    |

## Design Philosophy: Fail-Safe Normalization
The core principle of these mixins is that they **never raise exceptions**. 
If an input is invalid, it is silently replaced by a safe default (either from 
`SimpleExceptionData` or `SimpleExceptionSettings`). 

This ensures that the process of reporting an error never becomes the cause 
of a secondary, harder-to-debug internal error.

## Integration
These mixins are combined into the `SimpleException` class. Each provides a 
protected method (prefixed with `_`) that is called during `__init__` to 
populate the internal `SimpleExceptionData` structure.
"""