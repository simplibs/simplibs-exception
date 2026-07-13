"""
Tests for validate_location_blacklist — structural and element-level validation of filename exclusion filters.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_location_blacklist import (
    validate_location_blacklist,
)
from simplibs.exception.testing import assert_exception_function
from simplibs.exception.testing.asserts.functions.assert_function_valid_input import assert_function_valid_input


# -----------------------------------------------------------------------------
# 1. Valid Input Matrix
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("valid_input", [
    (),                               # Native empty tuple pass-through
    ("a.py", "b.py"),                 # Populated tuple
    ("single_element.py",),           # Single-element tuple
])
def test_validate_location_blacklist_valid_input(subtests, valid_input):
    """Verify that the validator successfully permits empty tuples and tuples consisting entirely of strings."""
    assert_function_valid_input(
        subtests,
        validate_location_blacklist,
        valid_params=(valid_input,),  # Safe encapsulation into the execution tuple
        verbose=False
    )


# -----------------------------------------------------------------------------
# 2. Invalid Input Matrix — Type Pollution (Container Level)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("invalid_container", [
    ["a.py", "b.py"],                 # Populated list structural container
    "a.py",                           # Raw string primitive
    123,                              # Numeric primitive
    {"a.py", "b.py"},                 # Native set container
    {"key": "value"},                 # Native dictionary container
])
def test_validate_location_blacklist_invalid_container(subtests, invalid_container):
    """Verify that non-tuple data types trigger a structural constraint error enforcing an immutable boundary."""
    assert_exception_function(
        subtests,
        validate_location_blacklist,
        invalid_params=(invalid_container,),  # Encapsulated on-the-fly into execution tuple
        valid_params=((),),                   # Gold-standard verification of an empty compliant state
        exception_type=SimpleExceptionSettingsError,
        value=invalid_container,              # Pure un-wrapped container for exact attribute matching
        label="LOCATION_BLACKLIST",
        expected="tuple[str, ...] — a tuple of strings containing filename patterns",
        problem="value is not a tuple",
        how_to_fix=(
            "Wrap the value in a tuple: ('filename.py',)",
            "To set an empty blacklist use an empty tuple: ()",
        ),
    )


# -----------------------------------------------------------------------------
# 3. Invalid Input Matrix — Element Constraints (Deep-Scan Evaluation)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("polluted_sequence, expected_extracted_errors", [
    (("a.py", 123, None), [123, None]),          # Standard mixed pollution
    ((True, "b.py"), [True]),                    # Boolean booby-trap (subclass of int)
    (((1, 2), "a.py"), [(1, 2)]),                 # Nested tuple pollution
])
def test_validate_location_blacklist_polluted_elements(subtests, polluted_sequence, expected_extracted_errors):
    """Verify that a deep-scan aggregates and reports all non-string elements inside the tuple simultaneously."""
    assert_exception_function(
        subtests,
        validate_location_blacklist,
        invalid_params=(polluted_sequence,),  # Encapsulated on-the-fly into execution tuple
        valid_params=((),),                   # Gold-standard verification of an empty compliant state
        exception_type=SimpleExceptionSettingsError,
        value=expected_extracted_errors,       # The validator extracts a list of bad elements
        label="LOCATION_BLACKLIST",
        expected="a tuple containing only string elements",
        problem="tuple contains invalid non-string elements",
        how_to_fix=(
            "Check all items — each one must be a string (str).",
            "Each item defines a file name pattern that will be skipped during location resolution.",
        ),
    )