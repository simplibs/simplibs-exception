"""
Tests for ToDictMixin — serialisation, UNSET exclusion, private attributes, and inheritance.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.exception._mixins.serializers.ToDict import ToDictMixin


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockBase(ToDictMixin):
    error_name: str
    message: str
    code: int
    _internal: str

    def __init__(self, error_name=UNSET, message=UNSET, code=UNSET, _internal="secret"):
        self.error_name = error_name
        self.message = message
        self.code = code
        self._internal = _internal


# -----------------------------------------------------------------------------
# to_dict
# -----------------------------------------------------------------------------

def test_all_set_values_are_serialized():
    """All provided public attributes must be present in the resulting dictionary."""
    obj = MockBase(error_name="AUTH_ERR", message="Access denied", code=403)
    assert obj.to_dict() == {
        "error_name": "AUTH_ERR",
        "message": "Access denied",
        "code": 403,
    }


def test_unset_values_are_excluded():
    """Attributes with an UNSET value must be omitted from the dictionary."""
    obj = MockBase(error_name="SIMPLE_ERR")
    result = obj.to_dict()
    assert result == {"error_name": "SIMPLE_ERR"}
    assert "message" not in result
    assert "code" not in result


def test_all_unset_returns_empty_dict():
    """If all attributes are UNSET, the result must be an empty dictionary."""
    obj = MockBase()
    assert obj.to_dict() == {}


def test_none_value_is_included():
    """None is not UNSET — it must be included in the result."""
    obj = MockBase(error_name=None)
    assert "error_name" in obj.to_dict()
    assert obj.to_dict()["error_name"] is None


def test_private_attributes_are_excluded():
    """Attributes starting with an underscore must be omitted."""
    obj = MockBase(error_name="ERR", _internal="secret")
    assert "_internal" not in obj.to_dict()


def test_inherited_annotations_are_included():
    """Annotations inherited from a parent class must be included."""
    class ChildData(MockBase):
        extra_info: str

        def __init__(self, extra_info=UNSET, **kwargs):
            super().__init__(**kwargs)
            self.extra_info = extra_info

    obj = ChildData(error_name="CHILD", extra_info="special")
    assert obj.to_dict() == {"error_name": "CHILD", "extra_info": "special"}