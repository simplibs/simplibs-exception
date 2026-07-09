from .deep_test_exception_class import deep_test_exception_class
from .is_exception_class import is_exception_class
from .is_exception_function import is_exception_function


_DESIGN_NOTES = """
# Testing Bulk Routing & Auditing Sub-Package

## Purpose
Manages structural type scanning, data signature routing, and full deep architectural audits 
required by the automated bulk testing sequence.

## Internal Components Registry

| Component                   | Type                 | Description                                                                         |
| :-------------------------- | :------------------- | :---------------------------------------------------------------------------------- |
| `deep_test_exception_class` | Function             | Performs comprehensive validation of exception class behavior and compliance.       |
| `is_exception_class`        | Function (TypeGuard) | Determines whether a runtime object is an exception class.                          |
| `is_exception_function`     | Function             | Detects callable exception test definitions and execution mappings.                 |
"""