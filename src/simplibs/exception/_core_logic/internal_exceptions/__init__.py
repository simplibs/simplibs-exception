from .SimpleExceptionInternalError import SimpleExceptionInternalError
from .SimpleExceptionModeError import SimpleExceptionModeError
from .SimpleExceptionSettingsError import SimpleExceptionSettingsError


_DESIGN_NOTES = """
# Internal Exceptions Sub-Package

## Purpose
This package encapsulates specific internal diagnostic exception classes used strictly within the 
framework boundaries to flag initialization failures, invalid settings configurations, or rendering faults.

## Internal Components Registry

| Component                        | Type            | Description                                                                            |
| :------------------------------- | :-------------- | :------------------------------------------------------------------------------------- |
| `SimpleExceptionInternalError`   | Exception Class | Base internal exception used for unrecoverable framework runtime failures.             |
| `SimpleExceptionSettingsError`   | Exception Class | Raised when global settings violate validation rules or required constraints.          |
| `SimpleExceptionModeError`       | Exception Class | Raised when a rendering engine violates the expected layout contract.                  |
"""
