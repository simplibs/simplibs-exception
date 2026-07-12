"""
Tests for validate_dynamic_cls_cache — validation of the internal multi-inheritance class cache.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_dynamic_cls_cache import (
    validate_dynamic_cls_cache,
)
from simplibs.exception.testing import assert_exception_function


# -----------------------------------------------------------------------------
# Invalid Input Matrix — Type Pollution & State Constraints
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("invalid_cache_state", [
    "bad-value",           # String primitive
    123,                   # Numeric primitive
    None,                  # Void object
    [], (),                # Other structural containers
    {"cached_key": str},   # Non-empty dict (CRITICAL: manual mutation attempt)
])
def test_validate_dynamic_cls_cache(subtests, invalid_cache_state):
    """Verify that any non-empty dict or invalid data type triggers a protective state violation.

    NOTE: An empty dictionary `{}` represents the only single permissible state for manual resets
          and is explicitly verified via the `valid_param` interceptor.
    """
    assert_exception_function(
        subtests,
        validate_dynamic_cls_cache,
        invalid_param=invalid_cache_state,
        valid_param={},  # Gold-standard verification of the only valid input state
        exception_type=SimpleExceptionSettingsError,
        value=invalid_cache_state,
        label="_dynamic_cls_cache",
        expected="an empty dict {} — for configuration and state reset routines only",
        problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
        how_to_fix=(
            "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
            "To clear this cache manually during hot-reloads or tests, assign an empty dict: "
            "SimpleExceptionSettings._dynamic_cls_cache = {}",
        ),
    )