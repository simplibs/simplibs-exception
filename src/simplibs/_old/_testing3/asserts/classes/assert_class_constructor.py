from typing import Any
# Outers
from ..fields import assert_exception_fields


def assert_class_constructor(
    subtests: Any,
    exc_class: type[Any],
    *,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Assert that an exception constructor accepts and stores all supported fields.

    Instantiates the exception class using the supplied constructor arguments and
    verifies that every provided value has been correctly propagated to the
    resulting exception instance.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to instantiate.
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The instantiated and validated exception object.
    """
    subintro = "test_class_constructor::"

    # Single Source of Truth: Define reference parameter matrix
    _message = "<message>"
    _value = "<value>"
    _label = "<label>"
    _expected = "<expected>"
    _problem = "<problem>"
    _context = "<context>"
    _how_to_fix = "<how_to_fix>"
    _error_name = "<ERROR_NAME>"
    _exception = ValueError("test exception")
    _get_location = False
    _skip_locations = ("<skip_locations>",)
    _oneline = True

    # Pass the matrix directly into the class constructor gate
    exc = exc_class(
        message=_message,
        value=_value,
        label=_label,
        expected=_expected,
        problem=_problem,
        context=_context,
        how_to_fix=_how_to_fix,
        error_name=_error_name,
        exception=_exception,
        get_location=_get_location,
        skip_locations=_skip_locations,
        oneline=_oneline,
    )

    # Validate that the instance layout perfectly mirrors the original reference data
    assert_exception_fields(
        subtests,
        exc,
        message=_message,
        value=_value,
        label=_label,
        expected=_expected,
        problem=_problem,
        context=_context,
        how_to_fix=_how_to_fix,
        error_name=_error_name,
        exception=_exception,
        get_location=_get_location,
        skip_locations=_skip_locations,
        oneline=_oneline,
        exact_match=True,
        verbose=verbose,
        intro=intro + subintro,
    )

    return exc


_DESIGN_NOTES = """
# assert_class_constructor (Constructor Propagation Audit)

## Purpose
Validates the state initialization boundaries of custom exception classes. It explicitly ensures that 
the exception's `__init__` constructor layer correctly intercepts, maps, and binds the entire 
framework-supported telemetry dataset to the active instance layout.

## Single Source of Truth Pattern
To guarantee complete diagnostic safety and eliminate duplicate literal typing, this engine 
implements a rigid internal variable matrix (prefixed with underscores, e.g., `_message`). 

This matrix is mapped symmetrically across two distinct execution boundaries:
1. **The Inbound Gate:** Fed into the custom exception factory constructor (`exc_class`).
2. **The Evaluation Gate:** Fed into the downstream `assert_exception_fields` blade.

This structural symmetry guarantees that any subtle mutation, data loss, or type truncation occurring 
inside the custom error constructor is instantly exposed by the cross-boundary verification check.
"""