from .assert_class_constructor import assert_class_constructor
from .assert_class_defaults import assert_class_defaults
from .assert_class_inheritance import assert_class_inheritance
from .assert_class_interface import assert_class_interface

__all__ = [
    "assert_class_constructor",
    "assert_class_defaults",
    "assert_class_inheritance",
    "assert_class_interface",
]

_DESIGN_NOTES = """
# Asserts Classes Sub-Engine Registry

## Purpose
Consolidates the four foundational, single-responsibility assertion blades used to evaluate 
the structural integrity, constructor propagation, fallback defaults, and public API interfaces 
of custom exception classes.

## Internal Components Registry

| Component                  | Type                   | Description                                                                           |
| :------------------------- | :--------------------- | :------------------------------------------------------------------------------------ |
| `assert_class_inheritance` | Structural Validation  | Validates class inheritance against `BaseException` and `SimpleExceptionData`.        |
| `assert_class_defaults`    | Reflection Validation  | Verifies class attributes and default state during parameterless initialization.      |
| `assert_class_constructor` | Initialization Testing | Tests the `__init__` flow across different initialization scenarios.                  |
| `assert_class_interface`   | API Validation         | Ensures serialization and string representation interfaces are implemented correctly. |
"""