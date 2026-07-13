"""
Tests for raise_unsupported_kwargs_parameter — validation routing and error payload building for Kwargs.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions import SimpleExceptionSettingsError
from simplibs.exception.testing import assert_exception_function
from simplibs.exception.testing.tools._validations.raise_unsupported_kwargs_parameter import (
    raise_unsupported_kwargs_parameter,
)

# -----------------------------------------------------------------------------
# Test Target Dummies
# -----------------------------------------------------------------------------

class DummyKwargsInstance:
    """Mock instance to simulate a Kwargs component context."""
    pass


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_multi_argument_overflow_raises_with_correct_metadata(subtests):
    """Verify diagnostics when more than one positional argument is supplied to the wrapper."""
    instance = DummyKwargsInstance()
    malformed_args = ({"a": 1}, {"b": 2})

    assert_exception_function(
        subtests,
        raise_unsupported_kwargs_parameter,
        invalid_params=(instance, malformed_args),
        exception_type=SimpleExceptionSettingsError,
        value=malformed_args,
        label="DummyKwargsInstance validation",
        problem="The wrapper accepts at most one positional mapping argument, received 2.",
        how_to_fix=(
            "Group multiple keyword arguments as a single dictionary: Kwargs({'a': 1, 'b': 2})",
            "Or pass them directly as named parameters: Kwargs(a=1, b=2)",
        ),
    )


def test_invalid_type_inversion_raises_with_correct_metadata(subtests):
    """Verify diagnostics when a single positional argument is passed but fails the Mapping check."""
    instance = DummyKwargsInstance()
    invalid_primitive_args = ("not-a-mapping",)

    assert_exception_function(
        subtests,
        raise_unsupported_kwargs_parameter,
        invalid_params=(instance, invalid_primitive_args),
        exception_type=SimpleExceptionSettingsError,
        value="not-a-mapping",
        label="DummyKwargsInstance validation",
        problem="Expected a valid collections.abc.Mapping structure, received 'str'.",
        how_to_fix=(
            "Ensure the positional argument implements the Mapping interface (e.g., a native dict).",
            "Primitives, lists, or tuples cannot be expanded into keyword arguments.",
        ),
    )