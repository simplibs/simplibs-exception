from dataclasses import dataclass
# Inners
from .SimpleExceptionInternalError import SimpleExceptionInternalError

@dataclass
class SimpleExceptionSettingsError(SimpleExceptionInternalError):
    """Raised when the global settings configuration encounters invalid options or invalid types."""
    error_name: str = "SETTINGS ERROR"


_DESIGN_NOTES = """
# SimpleExceptionSettingsError

## Purpose
A specialized, grouped internal exception triggered exclusively by validation failures, type mismatches, 
or invalid options within the global `SimpleExceptionSettings` configuration engine.

## Architectural Isolation
Internal library control faults must never utilize the primary `SimpleException` wrapper, as doing 
so would instantly introduce unbreakable circular import feedback loops. `SimpleExceptionSettingsError` 
natively inherits its structural isolation from `SimpleExceptionInternalError`, building directly on 
top of `SimpleExceptionData` and Python's primitive `Exception` class, completely decoupled from the 
live settings storage state.

## Operational Trigger Matrix
This error is primarily managed and emitted by the configuration metadata and validation layers (such 
as `settings_meta`). If a developer attempts to assign an invalid layout mode, an incorrect typewriter 
depth flag, or any un-sanitized property configuration option to the global manager, the framework 
blocks the corruption early and throws this error to protect downstream layout generators.

## Error Catching Patterns
Enables precise, decoupled exception trapping for application initialization boots or dynamic 
configuration hot-swaps:
```python
try:
    # ... dynamic configuration adjustments or library initialization ...
except SimpleExceptionSettingsError as err:
    # ... handle specialized configuration validation breaches ...
except SimpleExceptionInternalError:
    # ... fallback to catch any generic underlying framework fault ...
"""