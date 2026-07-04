from .ModeBase import ModeBase

__all__ = [
    "ModeBase",
]


_DESIGN_NOTES = """
# Abstract Mode Base Sub-Package

## Purpose
Isolates and houses the core abstract foundational class required for constructing compliant framework 
rendering engines.

## Exported Registry

| Component  | Type           | Description                                                                       |
| :--------- | :------------- | :-------------------------------------------------------------------------------- |
| `ModeBase` | Abstract Class | Provides the common rendering architecture and defines the `render` contract.     |
"""