import pytest

from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception.modes.PRETTY import PRETTY


def test_cannot_be_instantiated():
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings()


def test_system_blacklist_contains_expected_default_patterns():
    assert "<" in SimpleExceptionSettings._SYSTEM_BLACKLIST
    assert "simplibs/exception" in SimpleExceptionSettings._SYSTEM_BLACKLIST


def test_reset_restores_get_location_default():
    SimpleExceptionSettings.GET_LOCATION = 5
    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings.GET_LOCATION == 1


def test_reset_restores_value_truncation_length_default():
    SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH = 999
    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH == 70


def test_reset_restores_message_mode_default():
    from simplibs.exception.modes.SIMPLE import SIMPLE

    SimpleExceptionSettings.MESSAGE_MODE = SIMPLE
    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings.MESSAGE_MODE is PRETTY


def test_reset_clears_dynamic_cls_cache():
    # We can't assign a non-empty dict directly (the validator rejects it),
    # so we reach in behind the metaclass validation the same way the
    # framework itself does internally, then confirm reset() clears it.
    type.__setattr__(SimpleExceptionSettings, "_dynamic_cls_cache", {"fake": "entry"})
    assert SimpleExceptionSettings._dynamic_cls_cache == {"fake": "entry"}

    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings._dynamic_cls_cache == {}


def test_reset_sets_location_blacklist_to_empty_tuple_not_system_blacklist():
    """
    NOTE / POSSIBLE INCONSISTENCY: the class body's initial default for
    LOCATION_BLACKLIST is `_SYSTEM_BLACKLIST` (i.e. non-empty), but
    `reset()` explicitly sets it to `()` (empty) instead of restoring it to
    `_SYSTEM_BLACKLIST`. This test documents the actual current behavior of
    reset() -- worth double-checking whether this divergence is intentional.
    """
    SimpleExceptionSettings.LOCATION_BLACKLIST = ("something.py",)
    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings.LOCATION_BLACKLIST == ()
