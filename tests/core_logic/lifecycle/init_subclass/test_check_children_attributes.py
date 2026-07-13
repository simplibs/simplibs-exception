"""
Tests for check_children_attributes — contract verification and type checking for data schema subclasses.
"""
import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)
from simplibs.exception._core_logic.lifecycle.init_subclass.check_children_attributes import (
    check_children_attributes,
)
from simplibs.exception.testing import assert_exception_function
from simplibs.exception.testing.asserts.functions.assert_function_valid_input import assert_function_valid_input


# -----------------------------------------------------------------------------
# Test Blueprint Declarations (Static Schemas)
# -----------------------------------------------------------------------------

class Parent:
    """Mock baseline contract blueprint simulating the parent annotation schema definition."""
    error_name: str = "ERROR"
    count: int = 0
    _internal: str = "hidden"  # Private attribute - must be ignored entirely by the engine


# -----------------------------------------------------------------------------
# 1. Valid Contract Scenarios (Pass-Through Verification)
# -----------------------------------------------------------------------------

def test_valid_child_passes_silently(subtests):
    """Ensures that a concrete subclass conforming exactly to the parent blueprint types passes successfully."""
    class ChildGood(Parent):
        error_name: str = "GOOD"
        count: int = 5

    assert_function_valid_input(
        subtests,
        check_children_attributes,
        valid_params=(Parent, ChildGood),
        verbose=False
    )


def test_private_attributes_are_ignored_on_child(subtests):
    """Confirms that internal private variables on the subclass are skipped and do not trigger typo alerts."""
    class ChildWithPrivate(Parent):
        error_name: str = "GOOD"
        count: int = 5
        _private_thing: str = "should not matter"

    assert_function_valid_input(
        subtests,
        check_children_attributes,
        valid_params=(Parent, ChildWithPrivate),
        verbose=False
    )


def test_child_that_overrides_nothing_passes(subtests):
    """Validates that a bare subclass inheriting entirely from the parent without overrides is valid."""
    class ChildEmpty(Parent):
        pass

    assert_function_valid_input(
        subtests,
        check_children_attributes,
        valid_params=(Parent, ChildEmpty),
        verbose=False
    )


# -----------------------------------------------------------------------------
# 2. Structural & Typo Constraint Violations
# -----------------------------------------------------------------------------

def test_child_with_unknown_attribute_raises(subtests):
    """Verifies that defining an unmapped, unexpected attribute (typo) triggers a validation internal error."""
    class ChildUnknown(Parent):
        typo_attr: str = "oops"

    assert_exception_function(
        subtests,
        check_children_attributes,
        invalid_params=(Parent, ChildUnknown),
        exception_type=SimpleExceptionInternalError,
        value=["typo_attr"],
        label="class 'ChildUnknown'",
        expected="only attributes defined in 'Parent': ['error_name', 'count']",
        problem="class contains unknown attributes — likely a typo",
        context="parent attributes not defined in subclass: ['error_name', 'count']",
        how_to_fix=(
            "Check for typos in the attribute names.",
            "Permitted attributes are: ['error_name', 'count']",
        ),
    )


def test_private_parent_attributes_are_invisible_to_child_validation(subtests):
    """Architectural Edge Case: Private fields on the parent schema are strictly invisible.

    If a child defines an un-prefixed version matching a private parent field, it must be
    flagged as an unknown attribute typo.
    """
    class ChildTryingToExposePrivate(Parent):
        internal: str = "exposed"  # 'internal' does not exist in Parent's public contract

    assert_exception_function(
        subtests,
        check_children_attributes,
        invalid_params=(Parent, ChildTryingToExposePrivate),
        exception_type=SimpleExceptionInternalError,
        value=["internal"],
        label="class 'ChildTryingToExposePrivate'",
        expected="only attributes defined in 'Parent': ['error_name', 'count']",
        problem="class contains unknown attributes — likely a typo",
        context="parent attributes not defined in subclass: ['error_name', 'count']",
        how_to_fix=(
            "Check for typos in the attribute names.",
            "Permitted attributes are: ['error_name', 'count']",
        ),
    )


# -----------------------------------------------------------------------------
# 3. Type Mutation & Inversion Faults
# -----------------------------------------------------------------------------

def test_child_with_wrong_attribute_type_raises(subtests):
    """Guarantees that overriding a registered field with an incompatible data type triggers an execution halt."""
    class ChildTypeMismatch(Parent):
        count: int = "not-an-int"  # Violates the declared parent 'int' type schema

    assert_exception_function(
        subtests,
        check_children_attributes,
        invalid_params=(Parent, ChildTypeMismatch),
        exception_type=SimpleExceptionInternalError,
        value="not-an-int",
        label="'count' in class 'ChildTypeMismatch'",
        expected="int",
        problem="attribute has incorrect type — 1 error(s) found: ['count']",
        how_to_fix=(
            "Fix the type of attribute 'count' to 'int'.",
            "All attributes with type errors are listed in 'problem'.",
        ),
    )


def test_multiple_type_errors_reports_first_but_lists_all(subtests):
    """Ensures the error reporting strategy isolates the first type exception payload.

    Simultaneously, it transparently audits all invalid attributes inside the
    problem statement metadata.
    """
    class ChildMultipleErrors(Parent):
        error_name: int = 123
        count: str = "nope"

    assert_exception_function(
        subtests,
        check_children_attributes,
        invalid_params=(Parent, ChildMultipleErrors),
        exception_type=SimpleExceptionInternalError,
        value=123,  # Captures the value of the first discovered type mutation error
        label="'error_name' in class 'ChildMultipleErrors'",
        expected="str",
        problem="attribute has incorrect type — 2 error(s) found: ['error_name', 'count']",
        how_to_fix=(
            "Fix the type of attribute 'error_name' to 'str'.",
            "All attributes with type errors are listed in 'problem'.",
        ),
    )