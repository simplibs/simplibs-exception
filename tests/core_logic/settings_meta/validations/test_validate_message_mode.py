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
    """Confirms that the PRETTY engine singleton is accepted to activate rich terminal layouts."""
    assert validate_message_mode(PRETTY) is None


def test_simple_singleton_is_valid():
    """Confirms that the SIMPLE engine singleton is accepted to activate clean text layouts."""
    assert validate_message_mode(SIMPLE) is None


def test_log_singleton_is_valid():
    """Confirms that the LOG engine singleton is accepted to activate dense, telemetry-friendly layouts."""
    assert validate_message_mode(LOG) is None


def test_non_mode_instance_raises():
    """Guarantees that plain primitive types (like strings) are immediately blocked from the layout pipeline."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_message_mode("not-a-mode")


def test_mode_class_itself_not_instance_raises():
    """
    Ensures that passing the un-instantiated ModeBase blueprint class instead of a
    fully formed engine singleton instance triggers a terminal validation error.
    """
    from simplibs.exception.modes.base_class.ModeBase import ModeBase

    with pytest.raises(SimpleExceptionSettingsError):
        validate_message_mode(ModeBase)


def test_custom_user_defined_mode_instance_is_valid():
    """
    Architectural Integration Case: Verifies extensibility contract. A custom formatting
    engine built by a consumer successfully passes validation as long as it strictly
    inherits from the framework's baseline ModeBase class.
    """
    from simplibs.exception.modes.base_class.ModeBase import ModeBase

    class CustomJsonFormattingMode(ModeBase):
        """A custom external layout engine designed by an ecosystem consumer."""

        def _render(self, *args, **kwargs):
            """Fulfills the abstract contract required by the base architecture."""
            return "mock-rendered-string"

    # Now the instance can be safely born without raising a TypeError
    custom_instance = CustomJsonFormattingMode()

    # The validation guard must permit the custom plugin pass-through cleanly
    assert validate_message_mode(custom_instance) is None