from typing import Any

from simplibs.sentinels import UNSET, UnsetType
# Outers
from ....SimpleExceptionData import SimpleExceptionData
from ...tools import maybe_subtest


def assert_class_inheritance(
    subtests: Any,
    exc_class: type[Any],
    *,
    expected_parents: type[Any] | tuple[type[Any], ...] | UnsetType = UNSET,
    verbose: bool = True,
    intro: str = "",
) -> type[Any]:
    """Assert that an exception class satisfies the required inheritance contract.

    Verifies that the supplied class derives from both ``BaseException`` and
    ``SimpleExceptionData``, alongside optional custom polymorphic family blueprints.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to validate.
        expected_parents: An optional class type or a tuple of class types that the target
            exc_class must natively inherit from to satisfy custom polymorphic boundaries.
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

    # 3. Verify customized polymorphic architectural constraints if provided
    if expected_parents is not UNSET:
        with maybe_subtest(
            subtests,
            name=f"{intro}{subintro}test_custom_polymorphic_parents",
            verbose=verbose,
        ):
            # noinspection PyTypeChecker
            assert issubclass(exc_class, expected_parents)

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
3. **`expected_parents` Compliance (Dynamic Pass):** Evaluates specialized custom polymorphism constraints. 
   By providing a class or tuple of classes, developers can verify that deep architectural error branches 
   (e.g., `SimpleExceptionSettingsError`) remain safely matchable by their abstract parent groups 
   (e.g., `SimpleExceptionInternalError`).

## Pipeline Lifecycle Role
This routine serves as the entry-level sentinel within the composite `assert_exception_class` loop. 
By verifying the underlying type contract upfront, it guarantees that downstream layout inspections 
(which rely on introspection and reflection fields) can execute without throwing unpredictable, 
low-level attribute crashes.
"""