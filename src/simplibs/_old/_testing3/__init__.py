from .asserts import (
    assert_class_constructor,
    assert_class_defaults,
    assert_class_inheritance,
    assert_class_interface,
    assert_exception_class,
    assert_exception_fields,
    assert_exception_function,
    assert_function_callable,
    assert_function_raises,
    assert_function_valid_input,
)
from .containers import Kwargs, TestCase
from .exceptions_bulk_test import exceptions_bulk_test

__all__ = [
    "exceptions_bulk_test",
    "TestCase",
    "Kwargs",
    "assert_exception_class",
    "assert_exception_function",
    "assert_exception_fields",
    "assert_class_inheritance",
    "assert_class_defaults",
    "assert_class_constructor",
    "assert_class_interface",
    "assert_function_callable",
    "assert_function_valid_input",
    "assert_function_raises",
]

_DESIGN_NOTES = """
# Testing Framework Root Public API Gate

## Purpose
Acts as the ultimate high-level entry point for the exception testing subsystem. It implements 
a comprehensive Flattened Facade Pattern, gathering tools from `asserts/`, `containers/`, and 
the orchestration layer into a single, clean import location for test suite developers.

## 1. Orchestration & Data Core Registry
These components form the primary automation engine used to declare and execute massive 
test suites using data-driven matrix principles.

| Component              | Type              | Description                                                                 |
| :--------------------- | :---------------- | :-------------------------------------------------------------------------- |
| `exceptions_bulk_test` | Test Orchestrator | Routes mixed validation targets into appropriate execution flows.           |
| `TestCase`             | Test Container    | Encapsulates a functional evaluation scenario with inputs and expectations. |
| `Kwargs`               | Execution Guard   | Wraps keyword arguments and prevents parameter conflicts during execution.  |

## 2. Assertion Framework Registry (Hierarchical Sequence)
A complete library of structural and behavioral assertion check layers, ordered from high-level 
composite pipelines down to fine-grained atomic validation blades.

| Component                     | Type                   | Description                                                                                                  |
| :---------------------------- | :--------------------- | :----------------------------------------------------------------------------------------------------------- |
| `assert_exception_class`      | Composite Validation   | Executes the complete class validation flow including inheritance, defaults, initialization, and API checks. |
| `assert_exception_function`   | Composite Validation   | Executes complete function validation including execution flow, exceptions, and field verification.          |
| `assert_exception_fields`     | Field Validation       | Performs direct field and attribute matching on instantiated exception objects.                              |
| `assert_class_inheritance`    | Structural Validation  | Ensures required inheritance from `BaseException` and `SimpleExceptionData`.                                 |
| `assert_class_defaults`       | Reflection Validation  | Validates class-level defaults using parameterless instance inspection.                                      |
| `assert_class_constructor`    | Initialization Testing | Verifies constructor behavior across dynamic initialization scenarios.                                       |
| `assert_class_interface`      | Contract Validation    | Validates output types from formatting dunders and serialization methods.                                    |
| `assert_function_callable`    | Interface Validation   | Ensures the target callable can safely participate in the validation flow.                                   |
| `assert_function_valid_input` | Positive Execution     | Verifies stable execution using valid input scenarios.                                                       |
| `assert_function_raises`      | Negative Execution     | Confirms expected exception behavior for invalid input scenarios.                                            |
"""