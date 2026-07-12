from .Kwargs import Kwargs
from .maybe_subtest import maybe_subtest
from .Param import Param

__all__ = [
    "Kwargs",
    "maybe_subtest",
    "Param",
]

_DESIGN_NOTES = """
# Tools Sub-Engine Registry

## Purpose
Provides foundational architectural tools and utility decorators required by the 
testing engine. These components are designed to abstract away common testing 
patterns (such as conditional sub-test allocation and parameter type resolution), 
enabling a cleaner and more declarative test suite structure.

## Internal Components Registry

| Component      | Type                   | Description                                                |
| :------------- | :--------------------- | :--------------------------------------------------------- |
| `Kwargs`       | Semantic Wrapper       | Type-safe wrapper ensuring keyword arguments are expanded correctly. |
| `maybe_subtest`| Conditional Context    | Syntactic sugar for bypassing subtest overhead in non-verbose modes. |
| `Param`        | Semantic Wrapper       | Type-safe guard isolating a single parameter and preventing sequence unpacking. |

## Usage Note
These utilities are the bedrock of the engine's internal `asserts` and `bulk_test` logic. 
They follow a "zero-boilerplate" philosophy, allowing the higher-level assertion blades 
to remain readable and focused solely on validation logic.
"""