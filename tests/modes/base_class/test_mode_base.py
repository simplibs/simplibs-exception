"""
Tests for ModeBase — validation of the Template Method pattern, duck-typing contracts, and rendering pipelines.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionModeError import (
    SimpleExceptionModeError,
)
from simplibs.exception.modes.base_class.ModeBase import ModeBase
from simplibs.exception.testing import assert_exception_function
from simplibs.exception.testing.asserts.functions.assert_function_valid_input import assert_function_valid_input
from simplibs.exception.testing import Kwargs


# -----------------------------------------------------------------------------
# Test Target Stubs & Dummies
# -----------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------
# 1. Architectural & Lifecycle Constraints (ABC Mechanics)
# -----------------------------------------------------------------------------

def test_mode_base_cannot_be_instantiated_directly():
    """Guarantees that Python's native ABC mechanism prevents the direct instantiation of the abstract ModeBase blueprint."""
    with pytest.raises(TypeError):
        ModeBase()


def test_concrete_subclass_can_be_instantiated():
    """Confirms that a concrete subclass fulfilling the abstract SPI contract can be successfully initialized."""
    mode = _StubMode()
    assert isinstance(mode, ModeBase)


def test_repr_contains_class_name():
    """Verifies that the text representation blueprint dynamically wraps the active concrete subclass name."""
    mode = _StubMode()
    assert repr(mode) == "<_StubMode mode>"


# -----------------------------------------------------------------------------
# 2. Valid Input & Execution Fast-Paths
# -----------------------------------------------------------------------------

def test_render_delegates_to_render_implementation(subtests):
    """Verifies the Template Method pattern: calling the public render entry point properly dispatches to the internal layout logic."""
    mode = _StubMode()
    data = _ValidData()

    assert_function_valid_input(
        subtests,
        mode.render,
        valid_params=(data,),
    )


def test_render_validate_false_skips_the_structural_check(subtests):
    """Validates the internal Fast-Path route: bypassing validation via validate=False must completely skip attribute checks."""
    mode = _StubMode()
    data = _MissingAttrs()

    assert_function_valid_input(
        subtests,
        mode.render,
        valid_params=(data, Kwargs(validate=False)),
        verbose=False
    )


def test_render_passes_validation_when_required_attrs_present(subtests):
    """Confirms benevolent duck-typing: if the object contains at least 'message' and 'error_name', validation passes smoothly."""
    mode = _StubMode()
    data = _ValidData()

    assert_function_valid_input(
        subtests,
        mode.render,
        valid_params=(data,),
    )


# -----------------------------------------------------------------------------
# 3. Contract Violations & Structural Faults
# -----------------------------------------------------------------------------

def test_render_validates_by_default_and_raises_on_missing_attrs(subtests):
    """Ensures that the public safety net is active by default and throws a structured mode error upon encountering invalid data structures."""
    mode = _StubMode()
    invalid_data = _MissingAttrs()

    assert_exception_function(
        subtests,
        mode.render,
        invalid_params=(invalid_data,),
        valid_params=(_ValidData(),),  # Gold-standard verification of a compliant state
        exception_type=SimpleExceptionModeError,
        value=invalid_data,
        label="data",
        expected="an object satisfying SimpleExceptionDataProtocol",
        problem="the provided object does not match the expected exception data structure",
        how_to_fix=(
            "Pass an instance of SimpleExceptionData or any object implementing its protocol.",
            "For trusted internal calls, use validate=False to skip this check.",
        ),
    )


@pytest.mark.parametrize("incomplete_data", [
    type("_OnlyMessage", (), {"message": "text"})(),
    type("_OnlyErrorName", (), {"error_name": "CRITICAL_ERR"})(),
])
def test_validation_fails_if_only_one_required_attribute_is_present(subtests, incomplete_data):
    """Architectural Contract: Verifies that the duck-typing safety filter treats the required

    attribute pairs as a mandatory joint contract, blocking payloads that provide only one of them.
    """
    mode = _StubMode()

    assert_exception_function(
        subtests,
        mode.render,
        invalid_params=(incomplete_data,),
        valid_params=(_ValidData(),),
        exception_type=SimpleExceptionModeError,
        value=incomplete_data,
        label="data",
        expected="an object satisfying SimpleExceptionDataProtocol",
        problem="the provided object does not match the expected exception data structure",
        how_to_fix=(
            "Pass an instance of SimpleExceptionData or any object implementing its protocol.",
            "For trusted internal calls, use validate=False to skip this check.",
        ),
    )