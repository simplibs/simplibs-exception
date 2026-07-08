import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionModeError import (
    SimpleExceptionModeError,
)
from simplibs.exception.modes.base_class.ModeBase import ModeBase


class _StubMode(ModeBase):
    """A minimal concrete implementation stub used to isolate and test ModeBase mechanics."""
    def _render(self, data):
        return "stub-rendered"


class _MissingAttrs:
    """A deliberate contract violator that satisfies neither 'message' nor 'error_name'."""
    pass


class _ValidData:
    """A lightweight structural mock satisfying the absolute duck-typing minimum requirements."""
    message = "hi"
    error_name = "ERROR"


def test_mode_base_cannot_be_instantiated_directly():
    """Guarantees that Python's native ABC mechanism prevents the direct instantiation of the abstract ModeBase blueprint."""
    with pytest.raises(TypeError):
        ModeBase()


def test_concrete_subclass_can_be_instantiated():
    """Confirms that a concrete subclass fulfilling the abstract SPI contract can be successfully initialized."""
    mode = _StubMode()
    assert isinstance(mode, ModeBase)


def test_render_delegates_to_render_implementation():
    """Verifies the Template Method pattern: calling the public render entry point properly dispatches to the internal layout logic."""
    mode = _StubMode()
    result = mode.render(_ValidData(), validate=False)
    assert result == "stub-rendered"


def test_render_validates_by_default_and_raises_on_missing_attrs():
    """Ensures that the public safety net is active by default and throws a structured mode error upon encountering invalid data structures."""
    mode = _StubMode()
    with pytest.raises(SimpleExceptionModeError):
        mode.render(_MissingAttrs())


def test_render_validate_false_skips_the_structural_check():
    """Validates the internal Fast-Path route: bypassing validation via validate=False must completely skip attribute checks to ensure near-zero overhead."""
    mode = _StubMode()
    result = mode.render(_MissingAttrs(), validate=False)
    assert result == "stub-rendered"


def test_render_passes_validation_when_required_attrs_present():
    """Confirms benevolent duck-typing: if the object contains at least 'message' and 'error_name', validation passes smoothly."""
    mode = _StubMode()
    result = mode.render(_ValidData(), validate=True)
    assert result == "stub-rendered"


def test_repr_contains_class_name():
    """Verifies that the text representation blueprint dynamically wraps the active concrete subclass name for intuitive engineering visibility."""
    mode = _StubMode()
    assert repr(mode) == "<_StubMode mode>"


def test_validation_fails_if_only_one_required_attribute_is_present():
    """
    Architectural Contract: Verifies that the duck-typing safety filter treats the required
    attribute pairs as a mandatory joint contract, blocking payloads that provide only one of them.
    """
    mode = _StubMode()

    class _OnlyMessage:
        message = "text"

    class _OnlyErrorName:
        error_name = "CRITICAL_ERR"

    # 1. Object has message but lacks error_name -> must raise
    with pytest.raises(SimpleExceptionModeError) as exc_msg:
        mode.render(_OnlyMessage(), validate=True)
    assert "does not match the expected exception data structure" in exc_msg.value.problem

    # 2. Object has error_name but lacks message -> must raise
    with pytest.raises(SimpleExceptionModeError) as exc_err:
        mode.render(_OnlyErrorName(), validate=True)
    assert "does not match the expected exception data structure" in exc_err.value.problem