from typing import Any
# Outers
from ...._core_logic.internal_exceptions import SimpleExceptionSettingsError


def validate_dynamic_cls_cache(value: Any) -> None:
    """Verifies that the value is an empty dict — only allowed for cache reset."""
    if value != {}:
        raise SimpleExceptionSettingsError(
            value=value,
            label="_dynamic_cls_cache",
            expected="an empty dict {} — for configuration and state reset routines only",
            problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
            how_to_fix=(
                "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
                "To clear this cache manually during hot-reloads or tests, assign an empty dict: "
                "SimpleExceptionSettings._dynamic_cls_cache = {}",
            ),
        )


_DESIGN_NOTES = """
# validate_dynamic_cls_cache

## Purpose
Validates memory writes and state adjustments targeting the private `_dynamic_cls_cache` attribute 
within `SimpleExceptionSettings`. It acts as an internal guardrail protecting the shared type registry.

## Behavioral Constraints
This attribute is an internal computational pipeline. It is intentionally exposed with a leading underscore 
to maintain absolute design transparency, but manual arbitrary overrides are strictly prohibited. The only 
legitimate assignment value is a primitive empty dictionary `{}`. 

## Operational Context
The cache database is populated automatically at runtime by the performance optimization engine inside the 
`add_exception_type` lifecycle handler. Allowing a state overwrite exclusively for an empty dictionary `{}` 
enables safe framework cache invalidation sweeps, which are crucial during unit testing tear-downs, 
hot-swaps, or when triggering a global `SimpleExceptionSettings.reset()` command.
"""