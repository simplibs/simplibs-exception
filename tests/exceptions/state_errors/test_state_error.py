import pytest
from simplibs.exception.exceptions.base_error.SimpleError import SimpleError
from simplibs.exception.exceptions.state_errors.StateError import StateError
from simplibs.exception.testing import assert_exception_class


def test_state_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from SimpleError."""
    assert_exception_class(
        subtests,
        StateError,
        expected_parents=SimpleError,
    )