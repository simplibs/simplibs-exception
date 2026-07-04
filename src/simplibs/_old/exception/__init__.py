from .SimpleException import SimpleException
from .core import SimpleExceptionSettings, SimpleExceptionData
from .modes import (
    PRETTY,
    SIMPLE,
    ONELINE,
    LOG,
    ModeBase
)
from .tools import (
    bool_or_exception,
    raise_with_location_offset
)
from .tools.decorators import raise_location_offset

__all__ = [
    # Core class
    "SimpleException",
    "SimpleExceptionSettings",
    "SimpleExceptionData",
    # Modes
    "PRETTY",
    "SIMPLE",
    "ONELINE",
    "LOG",
    "ModeBase",
    # Tools
    "bool_or_exception",
    "raise_with_location_offset",
    "raise_location_offset",
]

_DESIGN_NOTES = """
# Package Entry Point

## Purpose
This module defines the public API for the `SimpleException` library. It 
exposes the primary exception class, configuration settings, and output modes 
while keeping internal implementation details (like mixins and private core 
logic) hidden from the end user.

## Exported Components

### 1. The Core
- **SimpleException**: The main exception class to be inherited or raised directly.
- **SimpleExceptionSettings**: Global configuration (colors, default limits, etc.).
- **SimpleExceptionData**: Data container for exception state, useful for typing.

### 2. Output Modes (Singletons)
Pre-configured instances that define how the exception message is rendered:
- **PRETTY**: Default framed output for terminal.
- **SIMPLE**: Plain text output without frames.
- **ONELINE**: Compact single-line output.
- **LOG**: Structured key=value format for machine processing.
- **ModeBase**: Abstract base for creating custom output formats.

### 3. Developer Tools
Utilities for handling call stack manipulation and result-based exceptions:
- **bool_or_exception**: Converts boolean results into raised exceptions.
- **raise_location_offset**: Decorator to shift the reported error location.
- **raise_with_location_offset**: Function for manual location shifting.

## Architecture Pattern
The library follows a "Flat API" pattern where all essential tools are 
accessible from the top-level package, while the source code remains 
highly modular and categorized in subdirectories.
"""
