import pytest
from simplibs.exception.exceptions.base_error.SimpleError import SimpleError
from simplibs.exception.exceptions.validations_errors.ValidationError import ValidationError
from simplibs.exception.testing import assert_exception_class


def test_validation_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from SimpleError."""
    assert_exception_class(
        subtests,
        ValidationError,
        expected_parents=SimpleError,
    )