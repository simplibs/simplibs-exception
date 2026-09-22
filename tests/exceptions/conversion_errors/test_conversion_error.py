import pytest
from simplibs.exception.exceptions.base_error.SimpleError import SimpleError
from simplibs.exception.exceptions.conversion_errors.ConversionError import ConversionError
from simplibs.exception.testing import assert_exception_class


def test_conversion_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from SimpleError."""
    assert_exception_class(
        subtests,
        ConversionError,
        expected_parents=SimpleError,
    )