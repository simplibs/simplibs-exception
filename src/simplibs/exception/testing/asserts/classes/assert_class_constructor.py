import pytest
from typing import Any
# Outers
from ...tools import maybe_subtest
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
    resulting exception instance. It also performs a basic string representation smoke check.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to instantiate.
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The instantiated and validated dummy exception object.
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

    # Pass the matrix directly into the class constructor gate (create a dummy test stub)
    dummy_exc = exc_class(
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

    # 1. Validate that the instance layout perfectly mirrors the original reference data
    assert_exception_fields(
        subtests,
        dummy_exc,
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

    # 2. String Smoke Check: Verify core diagnostic identities leak into str() representation.
    # We use resilient substring checks ('in') to avoid breaking when layout presentation or styles change.
    exc_str = str(dummy_exc)

    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_str_contains_error_name",
        verbose=verbose,
    ):
        assert _error_name in exc_str, (
            f"Constructor failed to propagate error_name into str().\n"
            f"Expected substring: {_error_name!r}\n"
            f"Actual string output: {exc_str!r}"
        )

    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_str_contains_message",
        verbose=verbose,
    ):
        assert _message in exc_str, (
            f"Constructor failed to propagate message into str().\n"
            f"Expected substring: {_message!r}\n"
            f"Actual string output: {exc_str!r}"
        )

    return dummy_exc


_DESIGN_NOTES = """
# assert_class_constructor (Constructor Propagation & String Smoke Audit)

## Purpose
Validates the state initialization boundaries of custom exception classes. It explicitly ensures that 
the exception's `__init__` constructor layer correctly intercepts, maps, and binds the entire 
framework-supported telemetry dataset to the active instance layout.

## Single Source of Truth Pattern
To guarantee complete diagnostic safety and eliminate duplicate literal typing, this engine 
implements a rigid internal variable matrix (prefixed with underscores, e.g., `_message`). 
This matrix is mapped symmetrically across the inbound factory gate and the downstream evaluation gate.

## Balanced String Evaluation (Smoke Testing vs. Layout Isolation)
A string representation audit (`str(dummy_exc)`) is executed to ensure that core identities 
are successfully exposed to the end-user. 
To prevent tight coupling with the elastic layout rendering engine (which dynamically reshapes 
output based on active presentation modes, tabs, or colors), the evaluation strictly utilizes 
fuzzy substring checking (`in` operator) confined exclusively to `error_name` and `message`. 
Exhaustive structural formatting tests are deliberately decoupled and isolated inside core framework layout suites.
"""