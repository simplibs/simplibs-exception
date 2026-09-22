# Inners
from ..base_error.SimpleError import SimpleError


class ValidationError(SimpleError):
    """A value or input failed to satisfy a required condition.

    Root of the validation-related exception family. Raised when something
    was checked against a rule — of any kind — and did not pass. More
    specific validation contexts (e.g. a function parameter) should subclass
    this rather than being raised directly.
    """
    pass


_DESIGN_NOTES = """
# ValidationError

## Purpose
General-purpose exception for "a value failed to satisfy a required
condition". This is the parent for every more specific validation scenario
(currently: `ParamError` for function/constructor parameters).

## Scope
Raise `ValidationError` directly only when the validated subject is not a
function parameter and no more specific subclass fits (e.g. validating a
parsed config block, an API response payload). If the invalid value is a
function or constructor parameter, raise `ParamError` instead so callers can
distinguish "bad input to my code" from "bad parameter passed to a function".
"""