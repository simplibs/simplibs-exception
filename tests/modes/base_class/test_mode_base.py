import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionModeError import (
    SimpleExceptionModeError,
)
from simplibs.exception.modes.base_class.ModeBase import ModeBase


class _StubMode(ModeBase):
    def _render(self, data):
        return "stub-rendered"


class _MissingAttrs:
    """An object that satisfies neither `message` nor `error_name`."""


class _ValidData:
    message = "hi"
    error_name = "ERROR"


def test_mode_base_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        ModeBase()


def test_concrete_subclass_can_be_instantiated():
    mode = _StubMode()
    assert isinstance(mode, ModeBase)


def test_render_delegates_to_render_implementation():
    mode = _StubMode()
    result = mode.render(_ValidData(), validate=False)
    assert result == "stub-rendered"


def test_render_validates_by_default_and_raises_on_missing_attrs():
    mode = _StubMode()
    with pytest.raises(SimpleExceptionModeError):
        mode.render(_MissingAttrs())


def test_render_validate_false_skips_the_structural_check():
    mode = _StubMode()
    # Would raise if validate=True; must succeed when validate=False.
    result = mode.render(_MissingAttrs(), validate=False)
    assert result == "stub-rendered"


def test_render_passes_validation_when_required_attrs_present():
    mode = _StubMode()
    result = mode.render(_ValidData(), validate=True)
    assert result == "stub-rendered"


def test_repr_contains_class_name():
    mode = _StubMode()
    assert repr(mode) == "<_StubMode mode>"
