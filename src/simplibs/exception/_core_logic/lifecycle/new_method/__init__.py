from .add_exception_type import add_exception_type


_DESIGN_NOTES = """
# Object Allocation Lifecycle Sub-Package

## Purpose
Manages low-level constructor allocation interventions during the `__new__` phase, injecting structural 
metadata and type tags before instance generation completes.

## Internal Components Registry

| Component            | Type     | Description                                                                    |
| :------------------- | :------- | :----------------------------------------------------------------------------- |
| `add_exception_type` | Function | Dynamically creates or reuses exception classes with additional base types.    |
"""
