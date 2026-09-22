import pytest
from simplibs.exception.exceptions.base_error.SimpleError import SimpleError
from simplibs.exception.exceptions.dependency_errors.DependencyError import DependencyError
from simplibs.exception.testing import assert_exception_class


def test_dependency_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from SimpleError."""
    assert_exception_class(
        subtests,
        DependencyError,
        expected_parents=SimpleError,
    )