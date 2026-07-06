"""
Tests for ToJsonMixin — JSON serialisation, UNSET exclusion, and non-serialisable types.
"""
import pytest
import json
from simplibs.sentinels import UNSET
from simplibs.exception.core._exception_mixins.serializers.ToDict import ToDictMixin
from simplibs.exception.core._exception_mixins.serializers.ToJson import ToJsonMixin


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockJsonBase(ToDictMixin, ToJsonMixin):
    error_name: str
    message: str
    exception_type: type

    def __init__(self, error_name=UNSET, message=UNSET, exception_type=UNSET):
        self.error_name = error_name
        self.message = message
        self.exception_type = exception_type


# -----------------------------------------------------------------------------
# to_json
# -----------------------------------------------------------------------------

def test_returns_valid_json_string():
    """The output must be a valid JSON string."""
    obj = MockJsonBase(error_name="JSON_ERR", message="Test message")
    json_str = obj.to_json()
    assert isinstance(json_str, str)
    json.loads(json_str)  # must not raise


def test_serialized_values_are_correct():
    """The JSON must contain the correct values."""
    obj = MockJsonBase(error_name="JSON_ERR", message="Test message")
    data = json.loads(obj.to_json())
    assert data["error_name"] == "JSON_ERR"
    assert data["message"] == "Test message"
    assert len(data) == 2


def test_unset_values_are_excluded():
    """UNSET values must not be present in the JSON output."""
    obj = MockJsonBase(error_name="ONLY_NAME")
    data = json.loads(obj.to_json())
    assert list(data.keys()) == ["error_name"]


def test_all_unset_returns_empty_json_object():
    """If all attributes are UNSET, the result must be '{}'."""
    obj = MockJsonBase()
    assert obj.to_json() == "{}"


def test_non_serializable_type_is_converted_to_string():
    """Types that JSON cannot serialise must be converted to a string via default=str."""
    obj = MockJsonBase(error_name="TYPE_ERR", exception_type=ValueError)
    data = json.loads(obj.to_json())
    assert "ValueError" in data["exception_type"]