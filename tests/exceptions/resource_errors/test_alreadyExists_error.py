import pytest
from simplibs.exception.exceptions.resource_errors.AlreadyExistsError import AlreadyExistsError
from simplibs.exception.exceptions.resource_errors.ResourceError import ResourceError
from simplibs.exception.testing import assert_exception_class


def test_already_exists_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from ResourceError."""
    assert_exception_class(
        subtests,
        AlreadyExistsError,
        expected_parents=ResourceError,
    )