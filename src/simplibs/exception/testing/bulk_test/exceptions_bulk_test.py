from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ..assert_exception_class import assert_exception_class
from ..assert_exception_function import assert_exception_function
from ..tools import maybe_subtest
# Inners
from .FunctionCase import FunctionCase
from ._utils import is_exception_class, is_exception_function


def exceptions_bulk_test(
    subtests: Any,
    items: list[Any],
    *,
    exact_match: bool = False,
    startswith: bool = False,
    verbose: bool = True,
    deep_check: bool = False,
) -> None:
    """Execute automated multi-format bulk verification pipelines across exceptions and routines.

    Iterates through a collection of declaration targets, dynamically routing each item
    based on its signature footprint into concrete runtime execution boundaries or deep
    architectural compliance audits.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        items: A heterogeneous collection of validation targets.
        exact_match: If True, enforces strict exact string equality.
        startswith: If True, validates that the actual value starts with the expected value.
        verbose: If True, executes each tracked item within an isolated subtest execution context.
        deep_check: If True, routes discovered raw exception classes through full
            compliance, constructor propagation, and serialization audits.

    Raises:
        AssertionError: If an item fails to match any supported format signatures.
    """

    for item in items:

        # 1. Process explicit composite testing contexts encapsulated as FunctionCase objects
        if isinstance(item, FunctionCase):
            intro = f"test_{item.func.__name__}::"

            item.run_test(
                subtests,
                exact_match=exact_match,
                startswith=startswith,
                verbose=verbose,
                intro=intro,
                deep_check=deep_check,
            )

        # 2. Process raw naked exception classes (Structural blueprint audits)
        elif is_exception_class(item):
            exc_class = item
            intro = f"test_{exc_class.__name__}::"

            assert_exception_class(
                subtests,
                exc_class,
                exact_match=exact_match,
                startswith=startswith,
                verbose=verbose,
                intro=intro,
                deep_check=deep_check,
            )

        # 3. Process raw parametric inline sequences wrapped in basic tuples
        elif is_exception_function(item):
            exc_class = item[0]
            func = item[1]
            raw_params = item[2:] if len(item) > 2 else UNSET
            intro = f"test_{func.__name__}::"

            assert_exception_function(
                subtests,
                func,
                invalid_param=raw_params,
                exception_type=exc_class,
                exact_match=exact_match,
                startswith=startswith,
                verbose=verbose,
                intro=intro,
                deep_check=False,
            )

        # 4. Fallback gate throwing strict alerts on invalid format tokens
        else:
            with maybe_subtest(subtests, name="unknown_item", verbose=verbose):
                raise AssertionError(f"Unsupported item signature footprint: {item!r}")


_DESIGN_NOTES = """
# exceptions_bulk_test (Public Testing Automation Matrix Orchestrator)

## Purpose
The primary orchestration suite designed to minimize testing code duplication. It behaves 
as an automated macro pipeline that accepts a high-level matrix profile of exception blueprints 
and validation hooks, standardizing error interception and compliance reporting.

## Comparison Modalities (Opt-in Architecture)
The engine defaults to substring inclusion (`in` operator) for maximum resilience against 
minor diagnostic text changes. Explicit modes can be enabled:
- **`exact_match=True`**: Enforces strict full-string equality.
- **`startswith=True`**: Validates based on prefix matching.

## Operational Modalities
1. **Shallow Mode (`deep_check=False`):** Optimized for fast CI passes. Checks functional intercept 
   states and standard zero-argument instantiation passes on naked classes.
2. **Deep Compliance Mode (`deep_check=True`):** Acts as an architectural gatekeeper. Discovered 
   exception classes are subjected to inheritance, constructor, and serialization audits.

## Practical Usage Matrix Example

```python
def test_complete_settings_subsystem_matrix(subtests):
    # A single test case evaluating an entire architecture seamlessly
    exceptions_bulk_test(
        subtests,
        items=[
            # 1. Shallow audit of a standalone exception class
            SimpleExceptionSettingsError,

            # 2. Functional invocation pass with zero parameters
            (SimpleExceptionSettingsError, trigger_global_settings_reset),

            # 3. Positional parametric validation check
            (SimpleExceptionSettingsError, validate_dynamic_cls_cache, "invalid_cache_key"),

            # 4. Complex named keyword argument unpacking pass
            (SimpleExceptionSettingsError, validate_message_mode, 999, {"strict": True})
        ],
        verbose=True,
        deep_check=True
    )

```

"""
