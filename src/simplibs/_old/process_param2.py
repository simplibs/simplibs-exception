from typing import Any
# Inners
from ....tools import Kwargs, Params



def process_param(
    param: Any
) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """Normalize a raw dynamic test parameter into standard execution arguments.

    Unpacks the provided parameter block into a structured `(args, kwargs)` tuple
    suitable for clean programmatical function invocation (`func(*args, **kwargs)`).
    """

    # Scenario 1: Sequence router handling multi-argument positional execution rows
    if isinstance(param, (Params, Kwargs)):
        return param.args_and_kwargs

    # Scenario 3: Standard atomic scalar payload or a standalone Param guard fallback
    else:
        return (param,), {}



_DESIGN_NOTES = """
# manage_param (Deterministic Matrix Parameter Router)

## Purpose
An internal signature-matching utility designed to normalize dynamic payload wrappers into standard 
Python invocation components (`*args`, `**kwargs`). It behaves as an isolation adapter layer allowing 
testing macros to evaluate verification targets with diverse signature requirements through a single variable.

## Conversion & Mapping Rules (Strict Determinism)

### 1. Explicit Keyword Wrapper (`Kwargs`)
Standalone `Kwargs` tokens are explicitly mapped into the `kwargs` dictionary space for named parameter 
injection. Raw Python dictionaries (`dict`) are **never** automatically expanded into keyword arguments.

### 2. Sequence Mapping (`tuple` / `list`)
Populated lists or tuples represent multi-positional argument vectors. If the last element within the 
sequence is a `Kwargs` token, it is extracted and unpacked into `kwargs`, while all preceding items 
form the core positional `args` chain. 

Empty lists or tuples are automatically treated as a single literal positional payload (i.e., preserved 
as an empty container argument) to easily support testing of empty sequence validation layers without 
requiring explicit wrapper initialization.

A deep-scan post-processing pass evaluates every extracted positional slot. If a slot contains an 
isolated `Param` guard, its inner value is transparently extracted, allowing multi-argument functions 
to accept raw container types natively without triggering flattening operations.

### 3. Scalar & Atomic Fallback
Any standard primitive, object instance, raw configuration dictionary (`dict`), or a standalone `Param` 
isolation guard is captured strictly as a singular literal positional payload. Standalone `Param` blocks 
unwrap their payload immediately here, guaranteeing that collections intended as single inputs pass through 
the sequence router safely without being broken apart into separate positional components.
"""