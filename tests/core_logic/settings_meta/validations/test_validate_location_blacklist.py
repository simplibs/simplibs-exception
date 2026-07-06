import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_location_blacklist import (
    validate_location_blacklist,
)


def test_empty_tuple_is_valid():
    assert validate_location_blacklist(()) is None


def test_tuple_of_strings_is_valid():
    assert validate_location_blacklist(("a.py", "b.py")) is None


def test_non_tuple_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_location_blacklist(["a.py", "b.py"])


def test_tuple_with_non_string_items_raises():
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_location_blacklist(("a.py", 123, None))

    assert exc_info.value.value == [123, None]


def test_string_instead_of_tuple_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_location_blacklist("a.py")
