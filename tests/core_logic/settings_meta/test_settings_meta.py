import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


def test_setting_a_valid_known_attribute_succeeds():
    """Confirms that assigning a fully authorized value to a known operational attribute passes cleanly and updates state."""
    SimpleExceptionSettings.GET_LOCATION = 2
    assert SimpleExceptionSettings.GET_LOCATION == 2


def test_setting_a_known_attribute_with_invalid_value_raises():
    """Guarantees that routing an invalid type payload to a valid attribute triggers the dynamic validation block."""
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings.GET_LOCATION = "invalid"


def test_setting_an_unknown_attribute_raises():
    """Verifies strict white-listing: writing an arbitrary, unauthorized, or typo-polluted attribute key is instantly blocked."""
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings.NOT_A_REAL_SETTING = 123


def test_mutating_system_blacklist_raises():
    """Ensures that the immutable system-level framework core metadata is fiercely protected against any overwrite attempts."""
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings._SYSTEM_BLACKLIST = ()


def test_system_blacklist_stays_intact_after_failed_mutation():
    """
    Architectural Contract: Validates isolation integrity. A failed or malicious attempt
    to mutate the protected system blacklist must leave the original underlying state entirely unaltered.
    """
    original = SimpleExceptionSettings._SYSTEM_BLACKLIST
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings._SYSTEM_BLACKLIST = ("hacked",)

    assert SimpleExceptionSettings._SYSTEM_BLACKLIST == original


def test_invalid_assignment_does_not_change_the_current_value():
    """
    Architectural Contract: Guarantees transactional execution. If a contextual validation algorithm
    fails mid-flight, the global memory stream state must roll back, preserving the pre-existing configuration intact.
    """
    original = SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH
    with pytest.raises(SimpleExceptionSettingsError):
        SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH = -1

    assert SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH == original


def test_dynamic_dispatcher_routes_to_correct_contextual_validators():
    """
    Architectural Contract: Verifies that the internal __setattr__ router accurately
    dispatches payloads to their specific contextual validation algorithms based on the mapping keys.
    """
    # 1. Trigger the MESSAGE_MODE path with a bad type and assert its unique validator response
    with pytest.raises(SimpleExceptionSettingsError) as exc_mode:
        SimpleExceptionSettings.MESSAGE_MODE = "invalid-mode-string"
    assert exc_mode.value.label == "MESSAGE_MODE"

    # 2. Trigger the VALUE_TRUNCATION_LENGTH path and ensure it routes to its own distinct guard
    with pytest.raises(SimpleExceptionSettingsError) as exc_trunc:
        SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH = "invalid-truncation-string"
    assert exc_trunc.value.label == "VALUE_TRUNCATION_LENGTH"