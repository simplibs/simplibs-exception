"""
Tests for SimpleExceptionSettings and SimpleExceptionSettingsMeta — defaults, validation, instantiation, reset, and cache protection.
Note: The metaclass is tested here because it cannot be meaningfully tested in isolation without Settings.
"""
import pytest
from simplibs.exception.settings.SimpleExceptionSettings import SimpleExceptionSettings
from simplibs.exception.settings._meta.validations.SimpleExceptionSettingsError import SimpleExceptionSettingsError
from simplibs.exception.modes import LOG, PRETTY


@pytest.fixture(autouse=True)
def reset_settings():
    """Automatically reset settings before each test."""
    SimpleExceptionSettings.reset()
    yield
    SimpleExceptionSettings.reset()


# -----------------------------------------------------------------------------
# Default values
# -----------------------------------------------------------------------------

def test_default_values():
    """Factory defaults must match the documentation."""
    assert SimpleExceptionSettings.DEFAULT_GET_LOCATION == 1
    assert SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST == ()
    assert SimpleExceptionSettings.DEFAULT_MESSAGE_MODE is PRETTY
    assert SimpleExceptionSettings._dynamic_cls_cache == {}


# -----------------------------------------------------------------------------
# Writing valid values
# -----------------------------------------------------------------------------

def test_valid_values_are_stored():
    """Valid values must be stored and readable."""
    SimpleExceptionSettings.DEFAULT_GET_LOCATION = 5
    SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = LOG

    assert SimpleExceptionSettings.DEFAULT_GET_LOCATION == 5
    assert SimpleExceptionSettings.DEFAULT_MESSAGE_MODE is LOG


# -----------------------------------------------------------------------------
# Value validation (Meta)
# -----------------------------------------------------------------------------

def test_invalid_value_raises_and_original_is_preserved():
    """An invalid value must raise an exception and the original value must remain unchanged."""
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings.DEFAULT_GET_LOCATION = "invalid"

    assert SimpleExceptionSettings.DEFAULT_GET_LOCATION == 1


def test_unknown_attribute_raises():
    """An unknown attribute must raise an exception — protection against typos."""
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        SimpleExceptionSettings.UNKNOWN_SETTING = True

    assert exc_info.value.value == "UNKNOWN_SETTING"
    assert "unknown attribute" in exc_info.value.problem


# -----------------------------------------------------------------------------
# Instantiation prevention
# -----------------------------------------------------------------------------

def test_instantiation_is_forbidden():
    """SimpleExceptionSettings must not be instantiable."""
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        SimpleExceptionSettings()

    assert "not intended to be instantiated" in exc_info.value.problem


# -----------------------------------------------------------------------------
# Reset
# -----------------------------------------------------------------------------

def test_reset_restores_all_defaults():
    """reset() must restore all attributes to their factory defaults."""
    SimpleExceptionSettings.DEFAULT_GET_LOCATION = False
    SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST = ("test",)
    SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = LOG

    SimpleExceptionSettings.reset()

    assert SimpleExceptionSettings.DEFAULT_GET_LOCATION == 1
    assert SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST == ()
    assert SimpleExceptionSettings.DEFAULT_MESSAGE_MODE is PRETTY
    assert SimpleExceptionSettings._dynamic_cls_cache == {}


# -----------------------------------------------------------------------------
# Cache protection
# -----------------------------------------------------------------------------

def test_cache_reset_with_empty_dict_passes():
    """Resetting the cache with an empty dict must pass."""
    SimpleExceptionSettings._dynamic_cls_cache = {}


def test_cache_write_with_data_raises():
    """Writing data to the cache must raise an exception."""
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings._dynamic_cls_cache = {"fake": "data"}