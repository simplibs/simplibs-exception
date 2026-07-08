import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_value_truncation_length import (
    validate_value_truncation_length,
)


def test_positive_int_is_valid():
    """Confirms that a standard positive integer is accepted to define the maximum character preview gate."""
    assert validate_value_truncation_length(70) is None


def test_zero_raises():
    """Guarantees that a zero value is rejected, as truncating text down to zero characters is an invalid layout state."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length(0)


def test_negative_raises():
    """Ensures that negative integer constraints instantly trigger an error since buffer slices must strictly be positive."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length(-5)


def test_bool_raises_even_though_it_is_technically_an_int():
    """
    Verifies the Defensive Type Gate: boolean flags (like True/False) must be strictly
    intercepted and rejected, preventing them from satisfying the implicit integer subclassing checks.
    """
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length(True)


def test_float_raises():
    """Validates that float values trigger a validation error, safeguarding the core string slicer engine."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length(70.5)


def test_string_raises():
    """Ensures that string representations of numbers are blocked fast, enforcing a rigid primitive type boundary."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length("70")


def test_error_payload_distinguishes_between_type_and_range_failures():
    """
    Architectural Contract: Verifies that the validator correctly routes failures,
    populating the 'problem' metadata with specific diagnostics for types versus value bounds.
    """
    # 1. Inspect a type pollution failure scenario
    with pytest.raises(SimpleExceptionSettingsError) as exc_type:
        validate_value_truncation_length("invalid-type")
    assert "value is not an integer" in exc_type.value.problem

    # 2. Inspect a value range constraint failure scenario
    with pytest.raises(SimpleExceptionSettingsError) as exc_range:
        validate_value_truncation_length(-10)
    assert "value is zero or negative" in exc_range.value.problem