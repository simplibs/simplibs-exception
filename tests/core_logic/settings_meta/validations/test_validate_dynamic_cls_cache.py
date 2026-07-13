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

@pytest.mark.parametrize("invalid_value", [
    "bad-value",            # String primitive
    123,                    # Numeric primitive
    (),                     # Void object / empty tuple as parameter value
    [],                     # List structural containers
    {"cached_key": str},    # Non-empty dict (CRITICAL: manual mutation attempt)
])
def test_validate_dynamic_cls_cache(subtests, invalid_value):
    """Verify that any non-empty dict or invalid data type triggers a protective state violation."""
    assert_exception_function(
        subtests,
        validate_dynamic_cls_cache,
        invalid_params=(invalid_value,),
        valid_params=({},),
        exception_type=SimpleExceptionSettingsError,
        value=invalid_value,
        label="_dynamic_cls_cache",
        expected="an empty dict {} — for configuration and state reset routines only",
        problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
        how_to_fix=(
            "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
            "To clear this cache manually during hot-reloads or tests, assign an empty dict: "
            "SimpleExceptionSettings._dynamic_cls_cache = {}",
        ),
    )