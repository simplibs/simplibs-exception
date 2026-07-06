import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.raise_unknown_settings_attribute_error import (
    raise_unknown_settings_attribute_error,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


def test_always_raises_settings_error():
    with pytest.raises(SimpleExceptionSettingsError):
        raise_unknown_settings_attribute_error(SimpleExceptionSettings, "TYPO_ATTR")


def test_error_carries_the_offending_name():
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_unknown_settings_attribute_error(SimpleExceptionSettings, "TYPO_ATTR")

    assert exc_info.value.value == "TYPO_ATTR"


def test_expected_lists_permitted_public_attributes():
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_unknown_settings_attribute_error(SimpleExceptionSettings, "TYPO_ATTR")

    expected = exc_info.value.expected
    assert "GET_LOCATION" in expected
    assert "MESSAGE_MODE" in expected
    # Private validators (leading underscore) must not leak into the public list.
    assert "_dynamic_cls_cache" not in expected
