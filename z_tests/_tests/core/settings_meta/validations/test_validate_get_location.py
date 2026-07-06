"""
Tests for validate_get_location — valid values, invalid values, and exception fields.
"""
import pytest
from simplibs.exception.core._internal_exceptions.SimpleExceptionSettingsError import SimpleExceptionSettingsError
from simplibs.exception.core._settings_meta.validations.validate_get_location import validate_get_location


# -----------------------------------------------------------------------------
# validate_get_location
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("value", [True, False, 0, 1, 2])
def test_valid_values_pass(value):
    """int and bool values must pass without raising."""
    validate_get_location(value)


@pytest.mark.parametrize("value", [
    "True",
    "1",
    None,
    1.0,
    [],
])
def test_invalid_values_raise(value):
    """Anything other than int or bool must raise SimpleExceptionSettingsError."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_get_location(value)


def test_exception_contains_correct_fields():
    """The raised exception must have correctly populated fields."""
    invalid = "True"
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_get_location(invalid)
    assert exc_info.value.value == invalid
    assert exc_info.value.value_label == "DEFAULT_GET_LOCATION"
    assert "int or bool" in exc_info.value.expected
    assert exc_info.value.error_name == "SETTINGS ERROR"