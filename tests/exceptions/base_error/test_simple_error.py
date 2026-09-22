import pytest
from simplibs.exception.exceptions.base_error.SimpleError import SimpleError
from simplibs.exception.testing import assert_exception_class


def test_simple_error_basic_contract(subtests):
    """Runs the universal validation suite for inheritance, defaults, constructor, and interface."""
    assert_exception_class(
        subtests,
        SimpleError,
    )