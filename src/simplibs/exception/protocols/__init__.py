from .ModeBaseProtocol import ModeBaseProtocol
from .SimpleExceptionProtocol import SimpleExceptionProtocol
from .SimpleExceptionDataProtocol import SimpleExceptionDataProtocol
from .SimpleExceptionSettingsProtocol import SimpleExceptionSettingsProtocol

__all__ = [
    "ModeBaseProtocol",
    "SimpleExceptionDataProtocol",
    "SimpleExceptionProtocol",
]


_DESIGN_NOTES = """
# Static Typing Protocols Sub-Package Entry Point

## Purpose
This package acts as the centralized structural typing matrix for the `SimpleException` library ecosystem. 
It defines the formal structural contracts (PEP 544 Protocols) governing core framework objects, 
enabling strict static analysis, compile-time verification, and safe cross-module type hinting.

## Structural Contracts Registry

| Protocol                          | Public | Description                                                                                   |
| :-------------------------------- | :----: | :-------------------------------------------------------------------------------------------- |
| `SimpleExceptionProtocol`         |   ✅   | Defines the complete public signature blueprint of the main exception class.                  |
| `SimpleExceptionDataProtocol`     |   ✅   | Models the read-only state container carrying the captured failure metadata context.          |
| `ModeBaseProtocol`                |   ✅   | Enforces the compliance matrix required for implementing custom layout rendering engines.     |
| `SimpleExceptionSettingsProtocol` |   ❌   | Internally maps the validation layout and core schemas guarding the global settings namespace. |

## Architectural Value & Decoupling
By relying on structural duck-typing via protocols rather than concrete class inheritance, the framework 
completely eliminates boot-phase initialization deadlocks and circular dependency circles. 

Downstream client applications can leverage these exported blueprints to design highly resilient, 
statically testable utility wrappers, validation chains, or custom formatting extensions without 
coupling their code directly to runtime execution segments.
"""