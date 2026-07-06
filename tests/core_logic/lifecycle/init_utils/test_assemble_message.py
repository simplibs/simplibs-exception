from simplibs.exception._core_logic.lifecycle.init_utils.assemble_message import (
    assemble_message,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings
from simplibs.exception.modes.ONELINE import ONELINE
from simplibs.exception.SimpleExceptionData import SimpleExceptionData


def test_oneline_true_uses_oneline_mode_regardless_of_settings():
    instance = SimpleExceptionData(label="my-label", message="hello")

    result = assemble_message(instance, oneline=True)

    assert result == ONELINE.render(instance, validate=False)


def test_oneline_false_uses_globally_configured_message_mode():
    instance = SimpleExceptionData(label="my-label", message="hello")

    result = assemble_message(instance, oneline=False)

    assert result == SimpleExceptionSettings.MESSAGE_MODE.render(instance, validate=False)


def test_oneline_false_reflects_changed_global_mode():
    from simplibs.exception.modes.SIMPLE import SIMPLE

    instance = SimpleExceptionData(label="my-label", message="hello")
    SimpleExceptionSettings.MESSAGE_MODE = SIMPLE

    result = assemble_message(instance, oneline=False)

    assert result == SIMPLE.render(instance, validate=False)
