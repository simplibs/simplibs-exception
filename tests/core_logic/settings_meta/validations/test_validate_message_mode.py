import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_message_mode import (
    validate_message_mode,
)
from simplibs.exception.modes.PRETTY import PRETTY
from simplibs.exception.modes.SIMPLE import SIMPLE
from simplibs.exception.modes.LOG import LOG


def test_pretty_singleton_is_valid():
    assert validate_message_mode(PRETTY) is None


def test_simple_singleton_is_valid():
    assert validate_message_mode(SIMPLE) is None


def test_log_singleton_is_valid():
    assert validate_message_mode(LOG) is None


def test_non_mode_instance_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_message_mode("not-a-mode")


def test_mode_class_itself_not_instance_raises():
    from simplibs.exception.modes.base_class.ModeBase import ModeBase

    with pytest.raises(SimpleExceptionSettingsError):
        validate_message_mode(ModeBase)
