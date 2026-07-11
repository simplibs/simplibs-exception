from .assert_exception_class import assert_exception_class
from .assert_exception_function import assert_exception_function
from .generate_bulk_tests import generate_bulk_tests

__all__ = [
    "assert_exception_class",
    "assert_exception_function",
    "generate_bulk_tests",
]

_DESIGN_NOTES = """
# Testing Automation Architecture Gateway (Public API)

## Purpose
Exposes a high-level, declarative validation and test-generation framework specifically engineered 
to audit exception state telemetry, handle automated intercept gates, and run deep compliance 
checks across custom `SimpleException` ecosystems.

## Public Tools Matrix

| Component                   | Target                 | Description                                                                 |
| :-------------------------- | :--------------------- | :-------------------------------------------------------------------------- |
| `assert_exception_class`    | Exception Class        | Instantiates an exception and validates its diagnostic state and attributes. |
| `assert_exception_function` | Function               | Verifies successful execution and expected exception handling in one helper. |
| `generate_bulk_tests`       | Batch Test Collection  | Executes bulk validation for collections of exception classes and functions. |
"""