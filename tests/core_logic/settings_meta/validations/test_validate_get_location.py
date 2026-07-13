"""
Tests for validate_get_location — validation of hybrid boolean flags and non-negative integer stack depths.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_get_location import (
    validate_get_location,
)
from simplibs.exception.testing import assert_exception_function
from simplibs.exception.testing.asserts.functions.assert_function_valid_input import assert_function_valid_input


# -----------------------------------------------------------------------------
# 1. Valid Input Matrix — Toggles and Non-Negative Depths
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("valid_input", [
    True, False,  # Standard boolean toggle switches
    0, 1, 5,      # Non-negative frame depth offsets (integers)
])
def test_validate_get_location_valid_input(subtests, valid_input):
    """Verify that the validator successfully permits all valid types and non-negative boundary values."""
    assert_function_valid_input(
        subtests,
        validate_get_location,
        valid_params=(valid_input,),  # Encapsulated into execution tuple
        verbose=False
    )


# -----------------------------------------------------------------------------
# 2. Invalid Input Matrix — Type Pollution
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("invalid_type", [
    "bad-value",  # String primitive
    2.5,          # Float values (even positive ones fail the exact type check)
    None,         # Void object
    (), []        # Empty structural containers
])
def test_validate_get_location_invalid_types(subtests, invalid_type):
    """Verify that passing an invalid type triggers a type-pollution settings error."""
    assert_exception_function(
        subtests,
        validate_get_location,
        invalid_params=(invalid_type,),  # Encapsulated into execution tuple
        valid_params=(True,),            # Gold-standard verification of a compliant state
        exception_type=SimpleExceptionSettingsError,
        value=invalid_type,              # Pure un-wrapped value passed for exact attribute matching
        label="GET_LOCATION",
        expected="int or bool (e.g., True, False, 1, 2)",
        problem="value is neither a boolean nor an integer",
        how_to_fix=(
            "Pass True or False to enable or disable location reporting.",
            "Pass a positive int to set the stack depth traversal limit (e.g., 1, 2).",
        ),
    )


# -----------------------------------------------------------------------------
# 3. Invalid Input Matrix — Range Constraints
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("invalid_range", [
    -1, -100, -9999
])
def test_validate_get_location_invalid_ranges(subtests, invalid_range):
    """Verify that passing a negative integer triggers a value-boundary check rejecting invalid stack depth."""
    assert_exception_function(
        subtests,
        validate_get_location,
        invalid_params=(invalid_range,),  # Encapsulated into execution tuple
        valid_params=(True,),             # Gold-standard verification of a compliant state
        exception_type=SimpleExceptionSettingsError,
        value=invalid_range,              # Pure un-wrapped value passed for exact attribute matching
        label="GET_LOCATION",
        expected="a non-negative integer (>= 0) or bool",
        problem="integer depth offset cannot be negative",
        how_to_fix=(
            "Pass a positive integer or 0 to define a valid stack traversal depth.",
            "Negative numbers are not supported by the Python frame inspection engine."
        )
    )