import pytest

from simplibs.exception.exceptions.validations_errors.ValidationError import ValidationError
from simplibs.exception.exceptions.validations_errors.builders.build_validation_error import (
    build_validation_error,
)
from simplibs.exception.testing import assert_exception_function


def _is_positive(x: int) -> bool:
    """Sample custom validation rule function."""
    return x > 0


def _raise_built_validation_error(rule, value, value_name=None, context=None):
    """Helper target function that builds and raises the ValidationError."""
    err = build_validation_error(
        rule=rule,
        value=value,
        value_name=value_name,
        context=context,
    )
    raise err


def test_build_validation_error_with_named_function(subtests):
    """Verify that build_validation_error creates a fully-populated ValidationError for a named function."""
    assert_exception_function(
        subtests,
        _raise_built_validation_error,
        invalid_params=(_is_positive, -5, "age", "user_registration"),
        exception_type=ValidationError,
        error_name="VALIDATION_ERROR",
        label="age",
        value=-5,
        expected="value satisfying callable condition '_is_positive'",
        problem="Value failed validation check executed by callable '_is_positive'.",
        context="user_registration",
        how_to_fix=("Provide a value that evaluates to True when passed to '_is_positive'.",),
        exception=ValueError,
        exact_match=True,
    )


def test_build_validation_error_with_lambda(subtests):
    """Verify that build_validation_error handles anonymous lambda functions correctly."""
    lambda_rule = lambda x: x != ""

    assert_exception_function(
        subtests,
        _raise_built_validation_error,
        invalid_params=(lambda_rule, "", "username"),
        exception_type=ValidationError,
        error_name="VALIDATION_ERROR",
        label="username",
        value="",
        expected="value satisfying callable condition '<lambda>'",
        problem="Value failed validation check executed by callable '<lambda>'.",
        how_to_fix=("Provide a value that evaluates to True when passed to '<lambda>'.",),
        exception=ValueError,
        exact_match=True,
    )