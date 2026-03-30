"""
Tests for check_children_class_attributes — valid subclasses, unknown attributes, and type errors.
"""
import pytest
from typing import Any
from simplibs.exception.exception._mixins.dunders._utils.check_children_class_attributes import check_children_class_attributes
from simplibs.exception.core import SimpleExceptionInternalError


# -----------------------------------------------------------------------------
# Test parent class
# -----------------------------------------------------------------------------

class Parent:
    name: str
    age: int
    data: Any
    _private: str  # must be ignored


# -----------------------------------------------------------------------------
# Valid cases
# -----------------------------------------------------------------------------

def test_valid_child_passes():
    """A correctly defined subclass must pass without raising."""
    class ValidChild:
        name = "Gemini"
        age = 1
        data = {"key": "value"}

    check_children_class_attributes(Parent, ValidChild)


def test_partial_child_passes():
    """A subclass does not need to define all parent attributes."""
    class MinimalChild:
        name = "Minimal"

    check_children_class_attributes(Parent, MinimalChild)


def test_private_attributes_in_child_are_ignored():
    """Private attributes on the subclass must be ignored."""
    class ChildWithPrivate:
        name = "Valid"
        _internal = True

    check_children_class_attributes(Parent, ChildWithPrivate)


def test_any_type_accepts_any_value():
    """An attribute annotated as Any must accept any value."""
    class AnyChild:
        data = 12345

    check_children_class_attributes(Parent, AnyChild)


# -----------------------------------------------------------------------------
# Unknown attributes (step 3)
# -----------------------------------------------------------------------------

def test_unknown_attribute_raises():
    """An unknown attribute must raise SimpleExceptionInternalError."""
    class ExtraChild:
        namme = "Typo here"  # typo in 'name'
        age = 20

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_class_attributes(Parent, ExtraChild)

    assert "namme" in exc_info.value.value
    assert "unknown attributes" in exc_info.value.problem


def test_unknown_attribute_context_contains_missing_parent_attrs():
    """Context must contain the parent attributes not defined in the subclass."""
    class ExtraChild:
        namme = "Typo"  # typo — 'name' is missing

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_class_attributes(Parent, ExtraChild)

    assert "name" in exc_info.value.context


# -----------------------------------------------------------------------------
# Type errors (step 4)
# -----------------------------------------------------------------------------

def test_wrong_type_raises():
    """An attribute with the wrong type must raise SimpleExceptionInternalError."""
    class BadTypeChild:
        name = 123  # should be str

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_class_attributes(Parent, BadTypeChild)

    assert exc_info.value.expected == "str"
    assert exc_info.value.value == 123
    assert "BadTypeChild" in exc_info.value.value_label


def test_multiple_type_errors_reported_in_problem():
    """When multiple type errors are present, problem must report their count."""
    class MultiErrorChild:
        name = 123    # should be str
        age = "old"   # should be int

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_class_attributes(Parent, MultiErrorChild)

    assert "2 error" in exc_info.value.problem


def test_complex_type_display():
    """The expected type must be displayed correctly even for non-trivial types."""
    class ParentWithList:
        items: list

    class ChildWithStr:
        items = "not a list"

    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        check_children_class_attributes(ParentWithList, ChildWithStr)

    assert exc_info.value.expected == "list"