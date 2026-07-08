import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)
from simplibs.exception._core_logic.lifecycle.init_subclass.check_children_attributes import (
    check_children_attributes,
)


class Parent:
    """Mock baseline contract blueprint simulating the parent annotation schema definition."""
    error_name: str = "ERROR"
    count: int = 0
    _internal: str = "hidden"  # Private attribute - must be ignored entirely by the engine


def test_valid_child_passes_silently():
    """Ensures that a concrete subclass conforming exactly to the parent blueprint types passes successfully."""
    class ChildGood(Parent):
        error_name: str = "GOOD"
        count: int = 5

    assert check_children_attributes(Parent, ChildGood) is None


def test_child_with_unknown_attribute_raises():
    """Verifies that defining an unmapped, unexpected attribute (typo) triggers a validation internal error."""
    class ChildUnknown(Parent):
        typo_attr: str = "oops"

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_attributes(Parent, ChildUnknown)

    assert "typo_attr" in exc_info.value.value


def test_child_with_wrong_attribute_type_raises():
    """Guarantees that overriding a registered field with an incompatible data type triggers an execution halt."""
    class ChildTypeMismatch(Parent):
        count: int = "not-an-int"  # Violates the declared parent 'int' type schema

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_attributes(Parent, ChildTypeMismatch)

    assert exc_info.value.value == "not-an-int"


def test_private_attributes_are_ignored_on_child():
    """Confirms that internal private variables on the subclass are skipped and do not trigger typo alerts."""
    class ChildWithPrivate(Parent):
        error_name: str = "GOOD"
        count: int = 5
        _private_thing: str = "should not matter"

    assert check_children_attributes(Parent, ChildWithPrivate) is None


def test_child_that_overrides_nothing_passes():
    """Validates that a bare subclass inheriting entirely from the parent without overrides is valid."""
    class ChildEmpty(Parent):
        pass

    assert check_children_attributes(Parent, ChildEmpty) is None


def test_multiple_type_errors_reports_first_but_lists_all():
    """
    Ensures the error reporting strategy isolates the first type exception payload
    while transparently auditing all invalid attributes inside the problem statement metadata.
    """
    class ChildMultipleErrors(Parent):
        error_name: int = 123
        count: str = "nope"

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_attributes(Parent, ChildMultipleErrors)

    assert "2 error(s)" in exc_info.value.problem


def test_private_parent_attributes_are_invisible_to_child_validation():
    """
    Architectural Edge Case: Verifies that private fields on the parent schema
    are strictly invisible. If a child defines an un-prefixed version matching
    a private parent field, it must be flagged as an unknown attribute typo.
    """
    class ChildTryingToExposePrivate(Parent):
        internal: str = "exposed"  # 'internal' does not exist in Parent's public contract

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_attributes(Parent, ChildTryingToExposePrivate)

    assert "internal" in exc_info.value.value
    assert "class contains unknown attributes" in exc_info.value.problem
