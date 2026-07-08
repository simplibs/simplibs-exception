from typing import Any, Union

from simplibs.exception._core_logic.lifecycle.init_subclass._type_matches import (
    _type_matches,
)


def test_any_always_matches():
    """
    Guarantees that the Any type annotation acts as an absolute wildcard bypass,
    matching any object, primitive, or None state instantly.
    """
    assert _type_matches(object(), Any) is True
    assert _type_matches(None, Any) is True
    assert _type_matches(123, Any) is True


def test_plain_type_matches_via_isinstance():
    """Validates standard type checks on plain, non-parameterized primitive types via isinstance evaluation."""
    assert _type_matches("hello", str) is True
    assert _type_matches(1, str) is False
    assert _type_matches(True, bool) is True


def test_union_pipe_syntax_matches_any_member():
    """Ensures that the PEP 604 pipe union syntax successfully recurses and matches when any member type aligns."""
    assert _type_matches("hello", str | int) is True
    assert _type_matches(1, str | int) is True
    assert _type_matches(1.5, str | int) is False


def test_typing_union_matches_any_member():
    """Verifies that the legacy typing.Union syntax evaluates identically to pipe union structures."""
    assert _type_matches("hello", Union[str, int]) is True
    assert _type_matches(1, Union[str, int]) is True
    assert _type_matches(1.5, Union[str, int]) is False


def test_optional_none_matches():
    """Validates that optional (Union with None) annotations correctly accept both the target type and None."""
    assert _type_matches(None, str | None) is True
    assert _type_matches("x", str | None) is True
    assert _type_matches(1, str | None) is False


def test_parameterized_container_checks_origin_only():
    """
    Architectural Contract: Confirms that parameterized tuples evaluate their origin
    container type only, intentionally avoiding deep element inspection for performance reasons.
    """
    assert _type_matches(("a", "b"), tuple[str, ...]) is True
    assert _type_matches((1, 2), tuple[str, ...]) is True  # Inner types are NOT verified by design
    assert _type_matches(["a", "b"], tuple[str, ...]) is False  # Fails due to invalid origin type


def test_parameterized_list_checks_origin_only():
    """Ensures that parameterized list structures validate the base array/list type constraints accurately."""
    assert _type_matches([1, 2, 3], list[str]) is True
    assert _type_matches((1, 2, 3), list[str]) is False


def test_nested_union_with_parameterized_container():
    """Validates complex composite types combining recursive union evaluation with structural container boundaries."""
    typ = tuple[str, ...] | None
    assert _type_matches(("a",), typ) is True
    assert _type_matches(None, typ) is True
    assert _type_matches("not-a-tuple", typ) is False


def test_custom_unset_type_boundary_matching():
    """
    Architectural Edge Case: Verifies that the recursive engine correctly evaluates
    our library-specific UnsetType token when combined inside complex layouts,
    matching fields that default to the UNSET sentinel.
    """
    from simplibs.exception.SimpleExceptionData import SimpleExceptionData

    # Extract the dynamic sentinels directly from the data layer blueprint
    unset_value = SimpleExceptionData().value
    unset_type = type(unset_value)

    annotation_layout = str | unset_type

    assert _type_matches(unset_value, annotation_layout) is True
    assert _type_matches("valid-string", annotation_layout) is True
    assert _type_matches(42, annotation_layout) is False