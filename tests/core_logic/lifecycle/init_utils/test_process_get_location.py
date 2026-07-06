from simplibs.exception._core_logic.lifecycle.init_utils.process_get_location import (
    process_get_location,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


def test_bool_true_is_passed_through():
    assert process_get_location(True) is True


def test_bool_false_is_passed_through():
    assert process_get_location(False) is False


def test_int_is_passed_through():
    assert process_get_location(3) == 3


def test_invalid_value_falls_back_to_settings_default():
    assert process_get_location("not-valid") == SimpleExceptionSettings.GET_LOCATION


def test_none_falls_back_to_settings_default():
    assert process_get_location(None) == SimpleExceptionSettings.GET_LOCATION


def test_reflects_changed_settings_default():
    SimpleExceptionSettings.GET_LOCATION = 5
    assert process_get_location(None) == 5
