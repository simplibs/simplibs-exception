import pytest
from simplibs.exception.exceptions.state_errors.InitializationError import InitializationError
from simplibs.exception.exceptions.state_errors.StateError import StateError
from simplibs.exception.testing import assert_exception_class


def test_initialization_error_basic_contract(subtests):
    """Runs the universal validation suite including inheritance from StateError."""
    assert_exception_class(
        subtests,
        InitializationError,
        expected_parents=StateError,
    )