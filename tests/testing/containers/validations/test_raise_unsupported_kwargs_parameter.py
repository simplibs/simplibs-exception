"""
Tests for raise_unsupported_kwargs_parameter — validation routing and error payload building for Kwargs.
"""
import pytest
from simplibs.exception._core_logic.internal_exceptions import SimpleExceptionSettingsError
from simplibs.exception.testing.containers._validations.raise_unsupported_kwargs_parameter import raise_unsupported_kwargs_parameter


# -----------------------------------------------------------------------------
# Test Target Dummies
# -----------------------------------------------------------------------------

class DummyKwargsInstance:
    """Mock instance to simulate a Kwargs component context."""
    pass


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_multi_argument_overflow_raises_with_correct_metadata():
    """Verify diagnostics when more than one positional argument is supplied to the wrapper."""
    instance = DummyKwargsInstance()
    malformed_args = ({"a": 1}, {"b": 2})

    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_unsupported_kwargs_parameter(instance, malformed_args)

    err = exc_info.value

    # Validate structural fields assigned by the exception broker
    assert err.label == "DummyKwargsInstance validation"
    assert err.value == malformed_args
    assert "at most one positional mapping argument" in err.problem

    # Verify presence of actionable hints
    joined_fix = " ".join(err.how_to_fix) if isinstance(err.how_to_fix, (list, tuple)) else err.how_to_fix
    assert "Group multiple keyword arguments" in joined_fix
    assert "Kwargs(a=1, b=2)" in joined_fix


def test_invalid_type_inversion_raises_with_correct_metadata():
    """Verify diagnostics when a single positional argument is passed but fails the Mapping check."""
    instance = DummyKwargsInstance()
    invalid_primitive_args = ("not-a-mapping",)

    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_unsupported_kwargs_parameter(instance, invalid_primitive_args)

    err = exc_info.value

    # Validate structural fields for type mismatches
    assert err.label == "DummyKwargsInstance validation"
    assert err.value == "not-a-mapping"
    assert "Expected a valid collections.abc.Mapping structure" in err.problem
    assert "received 'str'" in err.problem

    # Verify presence of actionable hints
    joined_fix = " ".join(err.how_to_fix) if isinstance(err.how_to_fix, (list, tuple)) else err.how_to_fix
    assert "Ensure the positional argument implements the Mapping interface" in joined_fix
    assert "Primitives, lists, or tuples cannot be expanded" in joined_fix