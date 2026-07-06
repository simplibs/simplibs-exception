import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


def test_setting_a_valid_known_attribute_succeeds():
    SimpleExceptionSettings.GET_LOCATION = 2
    assert SimpleExceptionSettings.GET_LOCATION == 2


def test_setting_a_known_attribute_with_invalid_value_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings.GET_LOCATION = "invalid"


def test_setting_an_unknown_attribute_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings.NOT_A_REAL_SETTING = 123


def test_mutating_system_blacklist_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings._SYSTEM_BLACKLIST = ()


def test_system_blacklist_stays_intact_after_failed_mutation():
    original = SimpleExceptionSettings._SYSTEM_BLACKLIST
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings._SYSTEM_BLACKLIST = ("hacked",)
    assert SimpleExceptionSettings._SYSTEM_BLACKLIST == original


def test_invalid_assignment_does_not_change_the_current_value():
    original = SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH = -1
    assert SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH == original
