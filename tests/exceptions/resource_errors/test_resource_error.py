import pytest
from simplibs.exception.exceptions.base_error.SimpleError import SimpleError
from simplibs.exception.exceptions.resource_errors.ResourceError import ResourceError
from simplibs.exception.testing import assert_exception_class


def test_resource_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from SimpleError."""
    assert_exception_class(
        subtests,
        ResourceError,
        expected_parents=SimpleError,
    )