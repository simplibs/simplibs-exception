# Inners
from .ValidationError import ValidationError


class ParamError(ValidationError):
    """A function or constructor parameter failed validation.

    Specialization of `ValidationError` scoped specifically to parameters —
    as opposed to validation of arbitrary data (config, payloads, etc.).
    """
    pass


_DESIGN_NOTES = """
# ParamError

## Purpose
Specialization of `ValidationError` for the single most common validation
scenario across the simplibs ecosystem: a function or constructor received
a parameter that does not satisfy its contract.

## Rationale
Across multiple simplibs libraries, the same pattern kept recurring —
a hand-rolled `ValidationError` raised specifically because of a bad
parameter. Promoting this to its own subclass here means every library in
the ecosystem imports the same `ParamError` instead of redefining an
equivalent one locally.
"""