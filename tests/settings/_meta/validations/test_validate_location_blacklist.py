"""
Tests for validate_location_blacklist — valid values, non-tuple inputs, and invalid items.
"""
import pytest
from simplibs.exception.settings._meta.validations.SimpleExceptionSettingsError import SimpleExceptionSettingsError
from simplibs.exception.settings._meta.validations.validate_location_blacklist import validate_location_blacklist


# -----------------------------------------------------------------------------
# validate_location_blacklist
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("value", [
    ("file.py", "other.py"),
    ("single.py",),
    (),
])
def test_valid_values_pass(value):
    """A tuple of strings and an empty tuple must pass without raising."""
    validate_location_blacklist(value)


@pytest.mark.parametrize("value", [
    ["file.py"],
    "file.py",
    None,
    {"file.py"},
])
def test_non_tuple_raises(value):
    """Anything other than a tuple must raise SimpleExceptionSettingsError."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_location_blacklist(value)


def test_non_tuple_exception_fields():
    """The exception for a non-tuple must have correctly populated fields."""
    invalid = ["file.py"]
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_location_blacklist(invalid)
    assert exc_info.value.value == invalid
    assert exc_info.value.value_label == "DEFAULT_LOCATION_BLACKLIST"
    assert "value is not a tuple" in exc_info.value.problem
    assert exc_info.value.error_name == "SETTINGS ERROR"


def test_bad_items_raises():
    """A tuple containing non-string items must raise SimpleExceptionSettingsError."""
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_location_blacklist(("fine.py", 123, None))
    assert exc_info.value.value == [123, None]
    assert exc_info.value.value_label == "DEFAULT_LOCATION_BLACKLIST"
    assert "item(s) that are not strings" in exc_info.value.problem
    assert exc_info.value.error_name == "SETTINGS ERROR"


def test_bad_items_count_in_problem():
    """The error message must contain the exact count of invalid items."""
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_location_blacklist(("ok.py", 1, 2, 3))
    assert "3 item" in exc_info.value.problem