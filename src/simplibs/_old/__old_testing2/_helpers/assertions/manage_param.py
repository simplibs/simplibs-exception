from typing import Any


def manage_param(param: Any) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """Normalize a raw dynamic test parameter into standard execution arguments.

    Unpacks the provided parameter block into a structured `(args, kwargs)` tuple
    suitable for clean programmatical function invocation (`func(*args, **kwargs)`).
    """

    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}

    # 1. Map dictionaries to keyword argument spaces
    if isinstance(param, dict):
        if param:
            kwargs = dict(param)
        else:
            # Handle empty dictionary as a literal positional payload
            args = (param,)

    # 2. Flatten sequences into standard positional argument tuples
    elif isinstance(param, (tuple, list)):
        if param:
            args = tuple(param)
        else:
            # Handle empty sequence containers as literal positional payloads
            args = (param,)

    # 3. Encapsulate primitives and scalars as single-item positional tuples
    else:
        args = (param,)

    return args, kwargs


_DESIGN_NOTES = """
# manage_param (Parameter Extraction Helper)

## Purpose
An internal signature-matching utility designed to normalize dynamic payload wrappers into standard 
Python invocation components (`*args`, `**kwargs`). It serves as an adapter layer allowing testing 
macros to evaluate validation targets with diverse call requirements through a unified configuration variable.

## Conversion & Mapping Rules

### 1. Dictionary Mapping (`dict`)
Populated dictionaries are directly mirrored into `kwargs` for named function injection. Empty dictionaries 
are treated as a singular literal input and encapsulated into `args` to preserve empty container testing.

### 2. Sequence Mapping (`tuple` / `list`)
Populated lists or tuples are converted into an immutable positional `args` chain. Empty sequences 
are safely wrapped into a literal positional tuple to bypass immediate unpacking side-effects.

### 3. Scalar Fallback
Pragmatic data primitives, custom instances, or framework tokens (such as `UNSET` or `None`) are 
automatically captured into a single-element positional tuple.
"""