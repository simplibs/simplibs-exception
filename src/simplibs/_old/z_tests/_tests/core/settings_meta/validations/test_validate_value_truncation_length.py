"""
Tests for validate_value_truncation_length — valid values, invalid values, and exception fields.
"""
import pytest
from simplibs.exception.core._internal_exceptions.SimpleExceptionSettingsError import SimpleExceptionSettingsError
from simplibs.exception.core._settings_meta.validations.validate_value_truncation_length import validate_value_truncation_length


# -----------------------------------------------------------------------------
# validate_value_truncation_length
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("value", [1, 50, 100, 1000])
def test_valid_values_pass(value):
    """Positive integers must pass without raising."""
    validate_value_truncation_length(value)


@pytest.mark.parametrize("value", [
    "100",  # string
    10.5,  # float
    None,  # None
    True,  # bool (must be excluded even if it is an int subclass)
    False,  # bool
    [],  # list
])
def test_invalid_types_raise(value):
    """Non-integer types (and booleans) must raise SimpleExceptionSettingsError."""
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_value_truncation_length(value)
    assert exc_info.value.problem == "value is not an integer"


@pytest.mark.parametrize("value", [0, -1, -100])
def test_invalid_range_raise(value):
    """Zero or negative integers must raise SimpleExceptionSettingsError."""
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_value_truncation_length(value)
    assert exc_info.value.problem == "value is zero or negative"


def test_exception_contains_correct_fields():
    """The raised exception must have correctly populated diagnostic fields."""
    invalid_val = 0
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_value_truncation_length(invalid_val)

    e = exc_info.value
    assert e.value == invalid_val
    assert e.value_label == "DEFAULT_VALUE_TRUNCATION_LENGTH"
    assert "positive integer greater than 0" in e.expected
    assert isinstance(e.how_to_fix, tuple)
    assert len(e.how_to_fix) == 2