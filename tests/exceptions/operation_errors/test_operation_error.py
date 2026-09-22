import pytest
from simplibs.exception.exceptions.base_error.SimpleError import SimpleError
from simplibs.exception.exceptions.operation_errors.OperationError import OperationError
from simplibs.exception.testing import assert_exception_class


def test_operation_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from SimpleError."""
    assert_exception_class(
        subtests,
        OperationError,
        expected_parents=SimpleError,
    )