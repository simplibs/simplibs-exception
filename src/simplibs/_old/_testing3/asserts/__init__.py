from .assert_exception_class import assert_exception_class
from .assert_exception_function import assert_exception_function
from .classes.assert_class_constructor import assert_class_constructor
from .classes.assert_class_defaults import assert_class_defaults
from .classes.assert_class_inheritance import assert_class_inheritance
from .classes.assert_class_interface import assert_class_interface
from .fields.assert_exception_fields import assert_exception_fields
from .functions.assert_function_callable import assert_function_callable
from .functions.assert_function_raises import assert_function_raises
from .functions.assert_function_valid_input import assert_function_valid_input

__all__ = [
    "assert_exception_class",
    "assert_exception_function",
    "assert_exception_fields",
    "assert_class_constructor",
    "assert_class_defaults",
    "assert_class_inheritance",
    "assert_class_interface",
    "assert_function_callable",
    "assert_function_raises",
    "assert_function_valid_input",
]

_DESIGN_NOTES = """
# Testing Assertions High-Level Flattened Facade Gate

## Purpose
Acts as the global public entry point for the entire assertion sub-system. It supports a dual-import 
topography (Flattened Facade Pattern): clients can either import any blade directly from this root gate 
for fast integration, or reference specific deep sub-packages (`.classes`, `.functions`, `.fields`) 
for rigid architectural explicitness.

## Universal Components Registry

| Component                     | Type                   | Description                                                                 |
| :---------------------------- | :--------------------- | :-------------------------------------------------------------------------- |
| `assert_exception_class`      | Exception Validation   | Validates complete exception class contracts, defaults, and initialization. |
| `assert_exception_function`   | Exception Execution    | Validates function execution, raised exceptions, and generated telemetry.   |
| `assert_exception_fields`     | Field Validation       | Validates required fields directly on instantiated exception objects.       |
| `assert_class_inheritance`    | Class Validation       | Validates inheritance against `BaseException` and `SimpleExceptionData`.    |
| `assert_class_defaults`       | Class State Validation | Verifies class attributes and default state during initialization.          |
| `assert_class_constructor`    | Constructor Validation | Tests constructor behavior across different initialization scenarios.       |
| `assert_class_interface`      | Interface Validation   | Ensures serialization and string representation interfaces are correct.     |
| `assert_function_callable`    | Function Validation    | Ensures the target execution object is callable before testing.             |
| `assert_function_valid_input` | Positive Execution     | Verifies successful execution using valid input scenarios.                  |
| `assert_function_raises`      | Negative Execution     | Verifies expected exception handling during invalid input scenarios.        |
"""