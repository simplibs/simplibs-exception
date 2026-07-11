from .compare_strings import compare_strings
from .is_exception_class import is_exception_class
from .is_exception_function import is_exception_function
from .manage_param import manage_param
from .maybe_subtest import maybe_subtest

__all__ = [
    "compare_strings",
    "is_exception_class",
    "is_exception_function",
    "manage_param",
    "maybe_subtest",
]

_DESIGN_NOTES = """
# Testing Automation Internal Helpers Engine

## Purpose
Consolidates low-level utility operations, type reflection predicates, parameter extraction 
routers, and conditional context proxies that power the upper assertion and bulk test execution layers.

## Internal Components Registry

| Component                | Description                                                                                                              |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **String Comparison**    | Strict equality and fuzzy substring matching utilities for diagnostic text.                                              |
| **Exception Detection**  | Type reflection helpers for validating Exception-based class structures.                                                 |
| **Function Detection**   | Type reflection utilities for identifying parameterized test execution flows.                                            |
| **Parameter Management** | Signature normalization helpers for converting dynamic payloads into strict Python execution blocks `(*args, **kwargs)`. |
| **Subtest Routing**      | Context routing utilities for switching between isolated subtest frames and direct execution paths.                      |
"""