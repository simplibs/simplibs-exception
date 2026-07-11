from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ..fields import assert_exception_fields


def assert_class_defaults(
    subtests: Any,
    exc_class: type[Any],
    *,
    exact_match: bool = True,
    startswith: bool = False,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Assert that an exception class correctly applies its default field values.

    Instantiates the exception class without constructor arguments and verifies
    that the resulting instance contains the same values as those defined on the
    class itself.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to validate.
        exact_match: Enables strict equality comparison.
        startswith: Enables prefix-based validation.
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The instantiated and validated exception object.
    """

    subintro = "test_class_defaults::"

    class_dict = exc_class.__dict__

    # Instantiate via raw parameterless initialization to capture the vanilla state
    exc = exc_class()

    return assert_exception_fields(
        subtests,
        exc,
        error_name=class_dict.get("error_name", UNSET),
        label=class_dict.get("label", UNSET),
        message=class_dict.get("message", UNSET),
        expected=class_dict.get("expected", UNSET),
        value=class_dict.get("value", UNSET),
        problem=class_dict.get("problem", UNSET),
        context=class_dict.get("context", UNSET),
        how_to_fix=class_dict.get("how_to_fix", UNSET),
        exception=class_dict.get("exception", UNSET),
        get_location=class_dict.get("get_location", UNSET),
        skip_locations=class_dict.get("skip_locations", UNSET),
        oneline=class_dict.get("oneline", UNSET),
        exact_match=exact_match,
        startswith=startswith,
        verbose=verbose,
        intro=intro + subintro,
    )


_DESIGN_NOTES = """
# assert_class_defaults (Static Metadata Reflection Verification)

## Purpose
Ensures that an exception class declaration remains pure and that its fallback properties correctly 
propagate down to individual instances upon zero-argument instantiation.

## Reflection Architecture Pattern
Instead of reading attributes directly from the instance (which might dynamically inherit fallback values), 
this engine extracts values via `exc_class.__dict__.get(...)`. This pattern allows the framework to explicitly 
isolate fields declared directly on the class body level.

## Comparison Modalities
This utility now supports the full suite of comparison logic (Exact Match, Starts With, Substring Inclusion),
allowing users to validate default exception states with varying levels of precision. This is particularly
useful when default error messages or problem descriptions are generated dynamically via base class 
factories.

## Composite Lifecycle Integration
This utility serves as a critical structural milestone within `assert_exception_class`. It validates 
that out-of-the-box exceptions (used for fast semantic drops or direct telemetry reports) behave 
deterministically without requiring explicit argument overrides.
"""