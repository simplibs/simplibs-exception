from typing import Any, Union

from simplibs.exception._core_logic.lifecycle.init_subclass._type_matches import (
    _type_matches,
)


def test_any_always_matches():
    assert _type_matches(object(), Any) is True
    assert _type_matches(None, Any) is True
    assert _type_matches(123, Any) is True


def test_plain_type_matches_via_isinstance():
    assert _type_matches("hello", str) is True
    assert _type_matches(1, str) is False
    assert _type_matches(True, bool) is True


def test_union_pipe_syntax_matches_any_member():
    assert _type_matches("hello", str | int) is True
    assert _type_matches(1, str | int) is True
    assert _type_matches(1.5, str | int) is False


def test_typing_union_matches_any_member():
    assert _type_matches("hello", Union[str, int]) is True
    assert _type_matches(1, Union[str, int]) is True
    assert _type_matches(1.5, Union[str, int]) is False


def test_optional_none_matches():
    assert _type_matches(None, str | None) is True
    assert _type_matches("x", str | None) is True
    assert _type_matches(1, str | None) is False


def test_parameterized_container_checks_origin_only():
    # tuple[str, ...] must only check isinstance against `tuple`,
    # inner element types are intentionally not verified.
    assert _type_matches(("a", "b"), tuple[str, ...]) is True
    assert _type_matches((1, 2), tuple[str, ...]) is True  # inner types NOT checked
    assert _type_matches(["a", "b"], tuple[str, ...]) is False  # wrong origin


def test_parameterized_list_checks_origin_only():
    assert _type_matches([1, 2, 3], list[str]) is True
    assert _type_matches((1, 2, 3), list[str]) is False


def test_nested_union_with_parameterized_container():
    typ = tuple[str, ...] | None
    assert _type_matches(("a",), typ) is True
    assert _type_matches(None, typ) is True
    assert _type_matches("not-a-tuple", typ) is False
