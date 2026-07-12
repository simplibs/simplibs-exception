"""
Tests for validate_value_truncation_length — runtime validation of text preview truncation boundaries.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_value_truncation_length import (
    validate_value_truncation_length,
)
from simplibs.exception.testing import assert_exception_function
from simplibs.exception.testing.asserts.functions.assert_function_valid_input import assert_function_valid_input


# -----------------------------------------------------------------------------
# 1. Valid Input Matrix
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("valid_length", [1, 50, 100, 1000])
def test_validate_value_truncation_length_valid_inputs(subtests, valid_length):
    """Verify that the validator successfully permits strictly positive integer metrics."""
    assert_function_valid_input(
        subtests,
        validate_value_truncation_length,
        valid_param=valid_length,
        verbose=False
    )


# -----------------------------------------------------------------------------
# 2. Invalid Input Matrix — Type Pollution
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("invalid_type", [
    "70",          # String representation
    70.5,          # Float values
    True, False,   # Boolean booby-traps (Python's implicit int subclasses)
    None, ()
])
def test_validate_value_truncation_length_invalid_types(subtests, invalid_type):
    """Verify that any non-integer input triggers a defensive type gate violation."""
    assert_exception_function(
        subtests,
        validate_value_truncation_length,
        invalid_param=invalid_type,
        exception_type=SimpleExceptionSettingsError,
        value=invalid_type,
        label="VALUE_TRUNCATION_LENGTH",
        expected="a positive integer (e.g., 50, 100, 200)",
        problem="value is not an integer",
        how_to_fix=(
            "Pass an integer value — e.g., 100, 200, 500.",
            "This value controls how many characters to show before truncating large values.",
        ),
    )


# -----------------------------------------------------------------------------
# 3. Invalid Input Matrix — Range Constraints
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("invalid_range", [0, -1, -500])
def test_validate_value_truncation_length_invalid_ranges(subtests, invalid_range):
    """Verify that integers equal to or below zero trigger a value range boundary violation."""
    assert_exception_function(
        subtests,
        validate_value_truncation_length,
        invalid_param=invalid_range,
        exception_type=SimpleExceptionSettingsError,
        value=invalid_range,
        label="VALUE_TRUNCATION_LENGTH",
        expected="a positive integer greater than 0",
        problem="value is zero or negative",
        how_to_fix=(
            "Pass a value greater than 0 — e.g., 50, 100.",
            "Recommended: 50-200 depending on your terminal width and layout preference.",
        ),
    )