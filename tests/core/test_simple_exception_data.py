"""
Tests for SimpleExceptionData — structure, default values, and initialization.
Based on the actual src/simplibs/exception structure.
"""
import pytest
from dataclasses import is_dataclass
from simplibs.sentinels import UNSET
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData


# -----------------------------------------------------------------------------
# Structure
# -----------------------------------------------------------------------------

def test_is_proper_dataclass():
    """SimpleExceptionData must be a proper dataclass."""
    assert is_dataclass(SimpleExceptionData)


def test_is_mutable():
    """SimpleExceptionData must be mutable — values are updated during processing."""
    data = SimpleExceptionData()
    data.error_name = "UPDATED"
    assert data.error_name == "UPDATED"


# -----------------------------------------------------------------------------
# Default Values
# -----------------------------------------------------------------------------

def test_default_values_are_correct():
    """All attributes must have the expected default values."""
    data = SimpleExceptionData()

    # Core Info
    assert data.error_name == "ERROR"
    assert data.exception is UNSET
    assert data._intercepted_exception is UNSET

    # Value Info
    assert data.value is UNSET
    assert data.value_label is UNSET

    # Description Info
    assert data.expected is UNSET
    assert data.problem is UNSET
    assert data.context is UNSET
    assert data.message is UNSET

    # Fix Info
    assert data.how_to_fix is UNSET

    # Location Info
    assert data._get_location is True
    assert data._skip_locations == ()
    assert data._cached_caller_info is UNSET

    # Output Mode
    assert data._oneline is False


# -----------------------------------------------------------------------------
# Custom Initialization
# -----------------------------------------------------------------------------

def test_custom_values_are_assigned():
    """Custom values passed at init must be stored correctly."""
    data = SimpleExceptionData(
        error_name="CUSTOM_ERROR",
        value=42,
        expected="a string",
    )

    assert data.error_name == "CUSTOM_ERROR"
    assert data.value == 42
    assert data.expected == "a string"
    assert data.message is UNSET  # others remain UNSET


# -----------------------------------------------------------------------------
# Underscore Convention
# -----------------------------------------------------------------------------

def test_internal_attributes_start_with_underscore():
    """Computed/internal attributes must follow the underscore naming convention."""
    internal_attrs = [
        "_intercepted_exception",
        "_get_location",
        "_skip_locations",
        "_cached_caller_info",
        "_oneline"
    ]
    for attr in internal_attrs:
        assert hasattr(SimpleExceptionData, attr), f"Missing attribute: {attr}"
        assert attr.startswith("_"), f"Attribute {attr} should start with underscore"