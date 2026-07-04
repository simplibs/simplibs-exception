# Core Classes
from .SimpleException import SimpleException
from .SimpleExceptionData import SimpleExceptionData
from .SimpleExceptionSettings import SimpleExceptionSettings

# Rendering Modes
from .modes import LOG, ONELINE, PRETTY, SIMPLE, ModeBase

# Structural Static Protocols
from .protocols import ModeBaseProtocol, SimpleExceptionDataProtocol, SimpleExceptionProtocol

# Developer Tools
from .tools import bool_or_exception, raise_location_offset, raise_with_location_offset

__all__ = [
    # Core Infrastructure
    "SimpleException",
    "SimpleExceptionData",
    "SimpleExceptionSettings",

    # Render Modes Singleton Engines
    "PRETTY",
    "SIMPLE",
    "ONELINE",
    "LOG",
    "ModeBase",

    # Advanced Developer Tooling
    "bool_or_exception",
    "raise_with_location_offset",
    "raise_location_offset",

    # Static Typing Type-Hinting Protocols
    "SimpleExceptionProtocol",
    "SimpleExceptionDataProtocol",
    "ModeBaseProtocol",
]

_DESIGN_NOTES = """
# Framework Root Entry Point

## Purpose
This module serves as the primary public API gateway for the `SimpleException` library ecosystem. 
It establishes a highly ergonomic, "Flat API" abstraction layer, exposing all operational 
classes, telemetry singletons, static typing blueprints, and execution tools from a single root namespace 
while keeping internal processing matrices completely encapsulated.

## Strategic Export Segmentation

### 1. Core Infrastructure
- `SimpleException`: The primary exceptions foundation designed to be caught or raised directly.
- `SimpleExceptionData`: The frozen data container carrying the complete state context of a captured failure, optimized for read-only extension pipelines.
- `SimpleExceptionSettings`: Global configuration registry managing framework behavior, color schemas, and truncation boundaries.

### 2. Render Singletons & Formatting Foundations
Pre-instantiated formatting engines governing how diagnostic payloads are serialized:
- `PRETTY`: Structured framed presentation tailored for terminal readouts.
- `SIMPLE`: Clean textual output stripped of structural borders.
- `ONELINE`: High-density single-row presentation.
- `LOG`: Key=value tokenized string serialization optimized for downstream log ingestion pipelines.
- `ModeBase`: Abstract architectural blueprint for deriving specialized custom layout rendering modules.

### 3. Developer Tooling Matrix
Advanced execution utilities modifying stack navigation or intercepting evaluation chains:
- `bool_or_exception`: Intercepts functional failure gates to return False or trigger a fully typed error instance.
- `raise_location_offset`: High-level declarative decorator automating runtime caller-site trace shifts.
- `raise_with_location_offset`: Low-level imperative functional helper providing explicit trace-shifting mechanics.

### 4. Static Typing Protocols
Explicit typing contracts mapped to internal system boundaries, enabling developers to write resilient, 
statically testable applications without binding to runtime code abstractions:
- `SimpleExceptionProtocol`: The strict structural type contract of the primary exception object.
- `SimpleExceptionDataProtocol`: Defines access methods for reading underlying stored context states.
- `ModeBaseProtocol`: Enforces interface validation when rolling custom rendering layers.

## Architecture Guidelines
By leveraging selective double-entry proxy definitions through internal sub-package `__all__` arrays, 
the system achieves an optimal balance between micro-modular repository file layouts and frictionless 
client consumption mechanics.
"""