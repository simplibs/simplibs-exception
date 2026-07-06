import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_get_location import (
    validate_get_location,
)


def test_bool_true_is_valid():
    assert validate_get_location(True) is None


def test_bool_false_is_valid():
    assert validate_get_location(False) is None


def test_positive_int_is_valid():
    assert validate_get_location(3) is None


def test_string_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_get_location("1")


def test_none_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_get_location(None)


def test_float_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_get_location(1.5)
