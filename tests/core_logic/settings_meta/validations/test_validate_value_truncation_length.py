import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_value_truncation_length import (
    validate_value_truncation_length,
)


def test_positive_int_is_valid():
    assert validate_value_truncation_length(70) is None


def test_zero_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length(0)


def test_negative_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length(-5)


def test_bool_raises_even_though_it_is_technically_an_int():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length(True)


def test_float_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length(70.5)


def test_string_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_value_truncation_length("70")
