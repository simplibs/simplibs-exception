from typing import Any
# Outers
from ....SimpleExceptionData import SimpleExceptionData
from ..._helpers import maybe_subtest


def assert_class_inheritance(
    subtests: Any,
    exc_class: type[Any],
    *,
    verbose: bool = True,
    intro: str = "",
) -> type[Any]:
    """Assert that an exception class satisfies the required inheritance contract.

    Verifies that the supplied class derives from both ``BaseException`` and
    ``SimpleExceptionData``.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to validate.
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The validated exception class.
    """

    subintro = "test_class_inheritance::"

    # 1. Verify that the target is a valid Python exception type
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_base_exception_inheritance",
        verbose=verbose,
    ):
        assert issubclass(exc_class, BaseException)

    # 2. Verify that the target incorporates the core framework data layout layer
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_simple_exception_data_inheritance",
        verbose=verbose,
    ):
        assert issubclass(exc_class, SimpleExceptionData)

    return exc_class


_DESIGN_NOTES = """
# assert_class_inheritance (Structural Hierarchy Gate)

## Purpose
Enforces the mandatory architectural multi-inheritance matrix required by custom framework errors. 
It ensures that compliance checks fail early (Fail-Fast) if a developer declares a custom exception 
but forgets to bind it to the necessary base building blocks.

## Verification Matrix
1. **`BaseException` Alignment:** Guarantees the class is natively recognized by Python's runtime 
   interpreter as an escapable error blueprint that can be triggered via `raise`.
2. **`SimpleExceptionData` Alignment:** Guarantees that the target implements the comprehensive framework 
   telemetry state manager, metadata trackers, and properties formatting machinery.

## Pipeline Lifecycle Role
This routine serves as the entry-level sentinel within the composite `assert_exception_class` loop. 
By verifying the underlying type contract upfront, it guarantees that downstream layout inspections 
(which rely on introspection and reflection fields) can execute without throwing unpredictable, 
low-level attribute crashes.
"""