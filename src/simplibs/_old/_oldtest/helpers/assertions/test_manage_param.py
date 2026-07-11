"""
Tests for manage_param — argument normalization, collection unpacking, and container literal fallbacks.
"""
from typing import Any
from simplibs.exception.testing._helpers.assertions.manage_param import manage_param


# -----------------------------------------------------------------------------
# Dictionary & Keyword Arguments Mapping
# -----------------------------------------------------------------------------

def test_populated_dict_maps_to_kwargs():
    """A populated dictionary must be fully mirrored into kwargs for named injection."""
    param = {"key": "value", "timeout": 30}
    args, kwargs = manage_param(param)

    assert args == ()
    assert kwargs == {"key": "value", "timeout": 30}


def test_empty_dict_treated_as_literal_arg():
    """An empty dictionary must be treated as a single literal positional argument."""
    param: dict[str, Any] = {}
    args, kwargs = manage_param(param)

    assert args == ({},)
    assert kwargs == {}


# -----------------------------------------------------------------------------
# Sequences & Positional Arguments Mapping
# -----------------------------------------------------------------------------

def test_populated_sequence_maps_to_args():
    """Populated tuples and lists must flatten into immutable positional args."""
    # Test tuple
    args_t, kwargs_t = manage_param(("abc", 123))
    assert args_t == ("abc", 123)
    assert kwargs_t == {}

    # Test list
    args_l, kwargs_l = manage_param(["xyz", False])
    assert args_l == ("xyz", False)
    assert kwargs_l == {}


def test_empty_sequence_treated_as_literal_arg():
    """Empty sequences must be wrapped as a singular positional payload."""
    # Test empty tuple
    args_t, kwargs_t = manage_param(())
    assert args_t == ((),)
    assert kwargs_t == {}

    # Test empty list
    args_l, kwargs_l = manage_param([])
    assert args_l == ([],)
    assert kwargs_l == {}


# -----------------------------------------------------------------------------
# Primitives, Scalars & Framework Tokens Fallback
# -----------------------------------------------------------------------------

def test_scalars_and_tokens_encapsulate_as_single_arg():
    """Primitives, custom objects, or tokens must wrap into a single-element positional tuple."""
    # String scalar
    args_s, _ = manage_param("flat_string")
    assert args_s == ("flat_string",)

    # Integer scalar
    args_i, _ = manage_param(42)
    assert args_i == (42,)

    # None value
    args_n, _ = manage_param(None)
    assert args_n == (None,)