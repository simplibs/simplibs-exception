import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)
from simplibs.exception._core_logic.lifecycle.init_subclass.check_children_attributes import (
    check_children_attributes,
)


class Parent:
    error_name: str = "ERROR"
    count: int = 0
    _internal: str = "hidden"  # private, must be ignored on the parent side too


def test_valid_child_passes_silently():
    class ChildGood(Parent):
        error_name: str = "GOOD"
        count: int = 5

    # Should not raise anything.
    assert check_children_attributes(Parent, ChildGood) is None


def test_child_with_unknown_attribute_raises():
    class ChildUnknown(Parent):
        typo_attr: str = "oops"

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_attributes(Parent, ChildUnknown)

    assert "typo_attr" in exc_info.value.value


def test_child_with_wrong_attribute_type_raises():
    class ChildTypeMismatch(Parent):
        count: int = "not-an-int"  # violates declared `int` annotation

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_attributes(Parent, ChildTypeMismatch)

    assert exc_info.value.value == "not-an-int"


def test_private_attributes_are_ignored_on_child():
    class ChildWithPrivate(Parent):
        error_name: str = "GOOD"
        count: int = 5
        _private_thing: str = "should not matter"

    # A private attribute not declared on the parent must not trigger
    # the "unknown attribute" branch.
    assert check_children_attributes(Parent, ChildWithPrivate) is None


def test_child_that_overrides_nothing_passes():
    class ChildEmpty(Parent):
        pass

    assert check_children_attributes(Parent, ChildEmpty) is None


def test_multiple_type_errors_reports_first_but_lists_all():
    class ChildMultipleErrors(Parent):
        error_name: int = 123
        count: str = "nope"

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_attributes(Parent, ChildMultipleErrors)

    # 'problem' text should mention that 2 errors were found.
    assert "2 error(s)" in exc_info.value.problem
