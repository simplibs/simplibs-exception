import pytest
from simplibs.exception.exceptions.validations_errors.ParamError import ParamError
from simplibs.exception.exceptions.validations_errors.ValidationError import ValidationError
from simplibs.exception.testing import assert_exception_class


def test_param_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from ValidationError."""
    assert_exception_class(
        subtests,
        ParamError,
        expected_parents=ValidationError,
    )