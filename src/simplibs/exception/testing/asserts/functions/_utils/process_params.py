from typing import Any
import pytest
# Inners
from ....tools import Kwargs


def process_params(
    params: tuple[Any, ...] | Kwargs
) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """Normalize a strict test parameter tuple into standard execution arguments.

    Enforces that all operational payloads are encapsulated in a tuple (representing *args)
    or a standalone Kwargs object. Unpacks them into a structured `(args, kwargs)` pair
    suitable for programmatic function invocation (`func(*args, **kwargs)`).
    """
    # Dynamic Scenario 1: Standalone keyword arguments (convenience fallback)
    if isinstance(params, Kwargs):
        return (), dict(params)

    # Core Scenario 2: Standard positional and optional trailing keyword arguments
    if isinstance(params, tuple):
        if params and isinstance(params[-1], Kwargs):
            # noinspection PyTypeChecker
            return params[:-1], dict(params[-1])
        return params, {}

    # Framework Guard: Enforce the explicit API contract to educate the developer
    pytest.fail(
        f"\n[Framework Guard] Invalid parameter container type detected!\n"
        f"Expected: tuple (representing *args) or Kwargs instance.\n"
        f"Actual:   {type(params).__name__} ({repr(params)})\n\n"
        f"💡 Tip: All test parameters must be wrapped in a tuple. Examples:\n"
        f"  - Single parameter:        invalid_params=(\"bad-value\",)\n"
        f"  - Keyword arguments only:  invalid_params=Kwargs(key=\"value\")\n"
        f"  - Nested tuple parameter:  invalid_params=((\"a\", \"b\"),)\n"
    )


_DESIGN_NOTES = """
# process_params (Deterministic Matrix Parameter Router)

## Purpose
An internal signature-matching utility designed to normalize explicit parameter payload containers 
into standard Python invocation components (`*args`, `**kwargs`). It behaves as a strict isolation 
adapter layer forcing test matrices to define call boundaries via predictable native tuples.

## Operational Architecture & Strict Safety Rules

The framework deliberately rejects implicit container guessing or automatic fallback wrapping. 
To guarantee absolute determinism and prevent flattening ambiguities (e.g., when a tuple is 
intended as a single argument vs. multiple arguments), the input contract enforces explicit signatures.

### 1. Explicit Keyword Wrapper (`Kwargs`)
A standalone `Kwargs` instance is routed entirely into the named `kwargs` dictionary space. 
Raw Python dictionaries (`dict`) are **never** automatically expanded into keyword arguments, 
ensuring dictionaries can be tested as primitive positional values safely.

### 2. Strict Sequence Mapping (`tuple`)
Tuples represent the literal positional argument vector (`*args`). 
- If the tuple contains a trailing `Kwargs` object, it is decoupled and unpacked into `kwargs`, 
  while all preceding elements form the positional `args` chain.
- If no trailing `Kwargs` are found, the entire tuple maps directly to positional `args`.
- Passing a tuple parameter as a single input requires wrapping it inside an outer master tuple: 
  `params=((item1, item2),)`.

### 3. Framework Guard Interception
Any input that does not comply with the `tuple` or `Kwargs` type boundary triggers an immediate 
`pytest.fail()` execution halt. This proactive assertion protects the test suite from confusing 
downstream `TypeError` traces and educates the developer on the unified API contract.
"""