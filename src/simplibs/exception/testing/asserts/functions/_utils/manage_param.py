from typing import Any
# Outers
from ....tools import Kwargs


def manage_param(
    param: Any
) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """Normalize a raw dynamic test parameter into standard execution arguments.

    Unpacks the provided parameter block into a structured `(args, kwargs)` tuple
    suitable for clean programmatical function invocation (`func(*args, **kwargs)`).
    """

    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}

    # 1. Map explicit semantic keyword wrappers directly to keyword argument spaces
    if isinstance(param, Kwargs):
        kwargs = dict(param)

    # 2. Flatten sequences into standard positional argument tuples with trailing check
    elif isinstance(param, (tuple, list)):
        if param:
            if isinstance(param[-1], Kwargs):
                args = tuple(param[:-1])
                # noinspection PyTypeChecker
                kwargs = dict(param[-1])
            else:
                args = tuple(param)
        else:
            args = (param,)

    # 3. Encapsulate scalars, primitives, or raw dictionaries as single-item positional payloads
    else:
        args = (param,)

    return args, kwargs


_DESIGN_NOTES = """
# manage_param (Deterministic Matrix Parameter Router)

## Purpose
An internal signature-matching utility designed to normalize dynamic payload wrappers into standard 
Python invocation components (`*args`, `**kwargs`). It behaves as an isolation adapter layer allowing 
testing macros to evaluate verification targets with diverse signature requirements through a single variable.

## Conversion & Mapping Rules (Strict Determinism)

### 1. Explicit Keyword Wrapper (`Kwargs`)
Naked or trailing `Kwargs` instances are explicitly mapped into the `kwargs` dictionary space for 
named parameter injection. Raw Python dictionaries (`dict`) are **never** automatically expanded into 
keyword arguments.

### 2. Sequence Mapping (`tuple` / `list`)
Populated lists or tuples are converted into an immutable positional `args` chain. If the last 
element within the sequence is a `Kwargs` token, it is extracted and unpacked into `kwargs`, while all 
preceding items become positional arguments. Empty sequences are wrapped into a literal positional tuple 
to protect empty container testing layers.

### 3. Scalar & Dictionary Fallback
Any standard primitive, object instance, or raw dictionary (`dict`) is treated strictly as a singular 
literal positional payload. This guarantees that functions accepting an ordinary mapping or configuration 
dictionary can be tested cleanly without accidental keyword expansion errors.
"""