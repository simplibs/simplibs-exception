from .assert_exception_class import assert_exception_class
from .assert_exception_function import assert_exception_function

from .bulk_test import exceptions_bulk_test, FuncCase

from .tools import Kwargs, maybe_subtest

from .asserts import (
    assert_exception_fields,
    assert_class_constructor,
    assert_class_defaults,
    assert_class_inheritance,
    assert_class_interface,
    assert_function_callable,
    assert_function_raises,
    assert_function_valid_input,
)

__all__ = [
    # High-Level Entry Points
    "assert_exception_class",
    "assert_exception_function",

    # Bulk Testing
    "exceptions_bulk_test",
    "FuncCase",

    # Utility Components
    "Kwargs",
    "maybe_subtest",

    # Low-Level Assertions
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
# Exception Testing Framework

## Purpose

This package provides a complete testing framework for validating both
`SimpleException` class hierarchies and the functional boundaries that
produce them.

It supports everything from low-level field verification to complete,
declarative bulk test suites.

## High-Level Entry Points

Primary orchestration functions intended for everyday use.

| Component                   | Description                                                                |
| :-------------------------- | :------------------------------------------------------------------------- |
| `assert_exception_class`    | Validates inheritance, constructor behavior, defaults, and public interface. |
| `assert_exception_function` | Validates functional execution, exception interception, and telemetry output. |

## Bulk Testing

Components used for reusable scenarios and large validation matrices.

| Component              | Description                                                              |
| :--------------------- | :----------------------------------------------------------------------- |
| `exceptions_bulk_test` | Executes heterogeneous collections of exception classes and function cases. |
| `FuncCase`         | Declarative container describing a reusable functional test scenario.      |


## Utility Components

Infrastructure helpers shared across the testing framework.

| Component       | Description                                                              |
| :-------------- | :----------------------------------------------------------------------- |
| `Kwargs`        | Explicit wrapper for keyword arguments inside parameterized test inputs.  |
| `maybe_subtest` | Context manager enabling optional pytest subtests with zero overhead.     |


## Low-Level Assertions

Fine-grained validation primitives used by the high-level orchestrators.

### Exception Fields

| Component                 | Description                                            |
| :------------------------ | :----------------------------------------------------- |
| `assert_exception_fields` | Validates individual exception telemetry properties.   |

### Exception Classes

| Component                   | Description                                                 |
| :-------------------------- | :---------------------------------------------------------- |
| `assert_class_constructor`  | Verifies constructor propagation of all telemetry fields.   |
| `assert_class_defaults`     | Validates default metadata declared on the exception class. |
| `assert_class_inheritance`  | Ensures compliance with the required inheritance contract.  |
| `assert_class_interface`    | Validates formatting, serialization, and public API.        |

### Functions

| Component                     | Description                                                    |
| :---------------------------- | :------------------------------------------------------------- |
| `assert_function_callable`    | Verifies that the supplied target is callable.                 |
| `assert_function_valid_input` | Confirms valid inputs execute without raising an exception.     |
| `assert_function_raises`      | Confirms invalid inputs raise the expected exception.           |
"""