import pytest
from simplibs.exception.testing.asserts.fields._utils._normalize_value import _normalize_value
from simplibs.sentinels import UNSET, UnsetType


def test_normalize_empty_states():
    """Verify None and UnsetType are translated into empty strings."""
    assert _normalize_value(None) == ""
    assert _normalize_value(UNSET) == ""
    assert _normalize_value(UnsetType()) == ""


def test_normalize_tuple_sequence():
    """Verify tuples are flattened into space-separated string blocks."""
    assert _normalize_value(("a", "b", "c")) == "a b c"


def test_normalize_string_passthrough():
    """Verify raw strings are returned without modification."""
    assert _normalize_value("hello") == "hello"


def test_normalize_scalar_coercion():
    """Verify objects and primitives are coerced to string format."""
    class CustomObj:
        def __str__(self):
            return "custom"

    assert _normalize_value(123) == "123"
    assert _normalize_value(CustomObj()) == "custom"