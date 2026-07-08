import json
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.SimpleExceptionData import SimpleExceptionData


def test_default_field_values():
    """Validates that a fresh instance adheres to the system defaults and sentinel states."""
    data = SimpleExceptionData()
    assert data.error_name == "ERROR"
    assert data.value is UNSET
    assert data.label is None
    assert data.get_location is True
    assert data.oneline is False


def test_caller_info_is_none_when_get_location_disabled():
    """Confirms location inspection is fully muted when disabled via flag."""
    data = SimpleExceptionData(get_location=False)
    assert data.caller_info is None


def test_caller_info_is_cached():
    """Verifies that the stack introspection engine behaves as a singleton-like cache after the first hit."""
    data = SimpleExceptionData(get_location=1)
    first_access = data.caller_info
    second_access = data.caller_info

    assert first_access is second_access


def test_to_dict_omits_unset_and_preserves_none():
    """Contract: Omit UNSET tokens in serialization, but preserve explicit None values for API clarity."""
    data = SimpleExceptionData(label="Test", message="Fail")
    serialized = data.to_dict()

    # Assert specific presence/absence
    assert serialized["label"] == "Test"
    assert serialized["expected"] is None  # Should be preserved
    assert "value" not in serialized  # Should be omitted as it remains UNSET


def test_to_json_handles_complex_types():
    """Ensures complex, non-JSON-native types gracefully degrade to their string representations."""

    class WeirdObject:
        def __str__(self): return "custom-repr"

    data = SimpleExceptionData(value=WeirdObject())
    parsed = json.loads(data.to_json())

    assert parsed["value"] == "custom-repr"


def test_caller_info_respects_skip_locations():
    """Validates frame filtering during stack traversal."""
    data = SimpleExceptionData(
        get_location=1,
        skip_locations=(__file__,),
    )
    # If the current file is skipped, the next available frame (if any) should be returned
    info = data.caller_info
    if info:
        assert info["path"] != __file__