import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.raise_unknown_settings_attribute_error import (
    raise_unknown_settings_attribute_error,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


def test_always_raises_settings_error():
    """Ensures that invoking the raiser consistently triggers a terminal SimpleExceptionSettingsError footprint."""
    with pytest.raises(SimpleExceptionSettingsError):
        raise_unknown_settings_attribute_error(SimpleExceptionSettings, "TYPO_ATTR")


def test_error_carries_the_offending_name():
    """Validates that the generated exception vehicle successfully carries the exact typo-polluted attribute name."""
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_unknown_settings_attribute_error(SimpleExceptionSettings, "TYPO_ATTR")

    assert exc_info.value.value == "TYPO_ATTR"


def test_expected_lists_permitted_public_attributes():
    """
    Verifies dynamic reflection accuracy: the 'expected' layout field must accurately list
    valid public attributes (like GET_LOCATION) while strictly hiding internal, private validators.
    """
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_unknown_settings_attribute_error(SimpleExceptionSettings, "TYPO_ATTR")

    expected = exc_info.value.expected

    # Public operational flags must be explicitly visible to the user
    assert "GET_LOCATION" in expected
    assert "MESSAGE_MODE" in expected

    # Private internal cache keys/validators with leading underscores must never leak
    assert "_dynamic_cls_cache" not in expected


def test_error_payload_contains_clear_remediation_instructions():
    """
    Architectural Contract: Verifies that the raised error contains the exact
    diagnostic problem and instruction blocks required for user remediation.
    """
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_unknown_settings_attribute_error(SimpleExceptionSettings, "UNKNOWN_KEY")

    err = exc_info.value
    joined_fix = " ".join(err.how_to_fix) if isinstance(err.how_to_fix, (list, tuple)) else err.how_to_fix

    assert err.label == "SimpleExceptionSettings"
    assert "unknown attribute" in err.problem
    assert "register its corresponding validation block" in joined_fix