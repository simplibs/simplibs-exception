from .is_exception_class import is_exception_class
from .is_exception_function import is_exception_function

_DESIGN_NOTES = """
# Bulk Test Sub-Engine Utilities Registry

## Purpose
Provides high-performance predicate checkers that determine the architectural category 
of a test subject (whether it is an exception class or an executable function). These 
utilities are essential for routing test subjects into their respective audit pipelines.

## Internal Components Registry

| Component             | Type               | Description                                              |
| :-------------------- | :----------------- | :------------------------------------------------------- |
| `is_exception_class`  | Predicate Engine   | Validates if a target adheres to the exception schema.   |
| `is_exception_function`| Predicate Engine   | Validates if a target is a valid functional audit hook.  |

## Access Restriction
These utilities are intended strictly for internal usage within `simplibs.exception.testing.bulk_test`. 
They are not part of the public API surface; therefore, they are not exported via `__all__`.
"""