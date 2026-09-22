import pytest
from simplibs.exception.exceptions.resource_errors.AccessError import AccessError
from simplibs.exception.exceptions.resource_errors.ResourceError import ResourceError
from simplibs.exception.testing import assert_exception_class


def test_access_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from ResourceError."""
    assert_exception_class(
        subtests,
        AccessError,
        expected_parents=ResourceError,
    )