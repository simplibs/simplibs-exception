import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_get_location import (
    validate_get_location,
)


def test_bool_true_is_valid():
    """Confirms that boolean True is accepted to globally activate call-site location reporting."""
    assert validate_get_location(True) is None


def test_bool_false_is_valid():
    """Confirms that boolean False is accepted to globally deactivate call-site location reporting."""
    assert validate_get_location(False) is None


def test_positive_int_is_valid():
    """Validates that a positive integer is permitted to explicitly set a customized stack depth limit."""
    assert validate_get_location(3) is None


def test_string_raises():
    """Guarantees that string-based numeric representations are blocked, preventing dynamic parsing ambiguities."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_get_location("1")


def test_none_raises():
    """Ensures that explicit None assignments are strictly intercepted, as global settings require a concrete runtime fallback."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_get_location(None)


def test_float_raises():
    """Verifies that floats are instantly rejected, since a non-integer stack frame lookup offset is programmatically invalid."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_get_location(1.5)


def test_boundary_integer_values_are_permitted_by_type_inspector():
    """
    Architectural Edge Case: Verifies that boundary integer layouts (such as zero
    and negative offsets) successfully pass through the validation filter without raising an error.
    """
    # Zero represents a structurally valid reference (the immediate execution frame anchor)
    assert validate_get_location(0) is None

    # Negative integers are permitted by the type signature for relative context mapping shifts
    assert validate_get_location(-1) is None