from dataclasses import dataclass
# Outers
from ...SimpleExceptionData import SimpleExceptionData


@dataclass
class SimpleExceptionInternalError(SimpleExceptionData, Exception):
    """Internal library exception — no validation, direct output only."""

    # Core identification override
    error_name: str = "INTERNAL ERROR"

    # --- REFERENCE PAYLOAD MATRIX (Quick declarative reference) ---
    # The attributes below are inherited from SimpleExceptionData.
    # Included as comments for instant developer visibility into available fields:
    #
    # value: Any = UNSET
    # label: str | None = None
    # expected: str | None = None
    # problem: tuple[str, ...] | str | None = None
    # context: tuple[str, ...] | str | None = None
    # how_to_fix: tuple[str, ...] | str | None = None

    def __post_init__(self):
        # 1. Render the message via PRETTY mode singleton
        from ...modes import PRETTY

        rendered_message = PRETTY.render(self, validate=False)

        # 2. Pass the formatted message to the native Exception layer.
        # Calling Exception.__init__ directly guarantees that even with dynamic
        # multi-inheritance shifts, the core string remains uncorrupted.
        Exception.__init__(self, rendered_message)


_DESIGN_NOTES = """
# SimpleExceptionInternalError

## Purpose
The base internal exception of the library — completely isolated from public `SimpleException` 
execution lifecycles. It inherits directly from `SimpleExceptionData` and Python's native `Exception`, 
relying only on the core `PRETTY` mode singleton for formatting.

## Isolation and Lazy Injection Pipeline
The `PRETTY` mode engine is imported lazily inside `__post_init__` to cut off circular dependency chains. 
Because `SimpleExceptionInternalError` resides inside the core internal logic block, a top-level import 
of the public mode matrix would trigger an infinite initialization loop.

The renderer is explicitly executed via `.render(self, validate=False)`:
- **Performance & Safety**: Internal errors are constructed by core library logic where data attributes 
  are structurally trusted. Skipping validation eliminates redundant overhead.
- **Loop Breaking**: Active validation would attempt to trigger protocol checks, re-importing internal 
  dependencies and causing a circular loop even through lazy evaluation layers.

The `PRETTY` mode layout is hardcoded by design. Internal subsystems must generate a predictable, 
bulletproof rich text matrix regardless of the active global configuration settings. During initialization 
or configuration faults, the global settings state may be corrupted, partial, or unstable.

## Group Base Class Architecture
Acts as the central operational boundary for all library-specific internal failures:
```python
class SimpleExceptionSettingsError(SimpleExceptionInternalError):
    error_name: str = "SETTINGS ERROR"

```

This enables seamless, grouped exception trapping across the application lifecycle:

```python
try:
    # ... boot library settings ...
except SimpleExceptionInternalError:
    # ... handle any internal framework initialization failure ...

```

## Declarative Attribute Blueprint

The commented-out attributes inside the class scope function as a high-visibility structural blueprint.
Without forcing developers to parse parent schemas or external specification documents, it highlights the
exact subset of descriptive properties that are contextually meaningful to supply during internal fault emission.
"""
