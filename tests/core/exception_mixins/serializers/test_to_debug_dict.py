"""
Tests for ToDebugDictMixin — public attributes, private attributes, unannotated attributes, and inheritance.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.core._exception_mixins.serializers.ToDict import ToDictMixin
from simplibs.exception.core._exception_mixins.serializers.ToDebugDict import ToDebugDictMixin


# Note on dunder attributes (__name):
# We deliberately do not test behaviour with dunder attributes (double underscore).
# Reason: Python name mangling converts __attr to _ClassName__attr, so the
# condition `not name.startswith("__")` is practically unreachable —
# get_type_hints already returns the attribute under its mangled single-underscore name.
# Additionally, dunder attributes on data classes are not a supported pattern
# and will never occur in real use with SimpleExceptionData.


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockDebugBase(ToDictMixin, ToDebugDictMixin):
    error_name: str
    _internal_info: str
    _hidden_detail: str

    def __init__(self, error_name=UNSET, _internal_info=UNSET, _hidden_detail=UNSET):
        self.error_name = error_name
        self._internal_info = _internal_info
        self._hidden_detail = _hidden_detail
        # Unannotated private attribute — simulates _rendered_message
        self._computed = "computed_value"


# -----------------------------------------------------------------------------
# to_debug_dict
# -----------------------------------------------------------------------------

def test_includes_public_and_private_attributes():
    """Must include both public and private attributes (with a single underscore)."""
    obj = MockDebugBase(error_name="DEBUG_ERR", _internal_info="some_trace")
    result = obj.to_debug_dict()
    assert result["error_name"] == "DEBUG_ERR"
    assert result["_internal_info"] == "some_trace"


def test_includes_unannotated_private_attributes():
    """Unannotated private attributes assigned in __init__ must be included."""
    obj = MockDebugBase(error_name="ERR")
    result = obj.to_debug_dict()
    assert "_computed" in result
    assert result["_computed"] == "computed_value"


def test_unset_values_are_excluded():
    """UNSET values must be omitted — both public and private."""
    obj = MockDebugBase(error_name="ERR")
    result = obj.to_debug_dict()
    assert "_hidden_detail" not in result


def test_all_unset_returns_empty_dict():
    """If all annotated attributes are UNSET, the result must contain only unannotated ones."""
    obj = MockDebugBase()
    result = obj.to_debug_dict()
    # _computed is always assigned in __init__
    assert result == {"_computed": "computed_value"}


def test_none_private_value_is_included():
    """A None value on a private attribute is not UNSET — it must be included."""
    obj = MockDebugBase(_internal_info=None)
    result = obj.to_debug_dict()
    assert "_internal_info" in result
    assert result["_internal_info"] is None


def test_inherited_private_attributes_are_included():
    """Private attributes inherited from a parent class must be included."""
    class ChildDebug(MockDebugBase):
        _child_secret: str

        def __init__(self, _child_secret=UNSET, **kwargs):
            super().__init__(**kwargs)
            self._child_secret = _child_secret

    obj = ChildDebug(
        error_name="CHILD",
        _internal_info="parent_secret",
        _child_secret="child_secret",
    )
    result = obj.to_debug_dict()
    assert result["error_name"] == "CHILD"
    assert result["_internal_info"] == "parent_secret"
    assert result["_child_secret"] == "child_secret"
    assert result["_computed"] == "computed_value"