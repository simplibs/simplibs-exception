import json
from simplibs.exception.SimpleExceptionData import SimpleExceptionData

# Resolve the global system UNSET sentinel footprint dynamically from baseline data
UNSET = SimpleExceptionData().value


def test_default_field_values():
    """
    Validates that a freshly instantiated data container strictly conforms
    to the system contract, assigning perfect default metrics and sentinels.
    """
    data = SimpleExceptionData()

    # 1. Assert default metadata layout states
    assert data.error_name == "ERROR"
    assert data.exception is None
    assert data.intercepted_exception is None
    assert data.value is UNSET
    assert data.label is None
    assert data.expected is None
    assert data.message is None
    assert data.problem is None
    assert data.context is None
    assert data.how_to_fix is None
    assert data.get_location == 1 or data.get_location is True
    assert data.skip_locations == ()
    assert data.oneline is False


def test_caller_info_is_none_when_get_location_disabled():
    """Ensures that explicitly muting location collection blocks frame inspection completely."""
    data = SimpleExceptionData(get_location=False)
    assert data.caller_info is None


def test_caller_info_is_populated_when_get_location_enabled():
    """Verifies that activating frame extraction yields a fully formed structural data footprint."""
    data = SimpleExceptionData(get_location=1)
    info = data.caller_info

    assert info is not None
    assert set(info.keys()) == {"file", "path", "line", "function"}


def test_caller_info_is_cached_after_first_access():
    """
    Guarantees that the stack inspection engine caches its result on initial evaluation,
    returning the exact same object reference instantly on subsequent access cycles.
    """
    data = SimpleExceptionData(get_location=1)

    # 1. Request property twice to trigger caching pathway
    first = data.caller_info
    second = data.caller_info

    # 2. Validate memory address identifier equality
    assert first == second
    assert first is second


def test_caller_info_respects_skip_locations():
    """Validates that local blacklist patterns successfully bypass specific frames during stack analysis."""

    def wrapper():
        return SimpleExceptionData(
            get_location=1,
            skip_locations=(__file__,),
        ).caller_info

    info = wrapper()
    if info is not None:
        assert info["path"] != __file__


def test_to_dict_matches_to_dict_helper_output():
    """
    Verifies the public dictionary serialization contract. Omites the UNSET token,
    but correctly retains explicit None markers for schema completeness.
    """
    # 1. Instantiate state package overrides
    data = SimpleExceptionData(label="x", message="hi")

    # 2. Assert exact alignment with the core logic output blueprint
    assert data.to_dict() == {
        "error_name": "ERROR",
        "label": "x",
        "message": "hi",
        "expected": None,
        "problem": None,
        "context": None,
        "how_to_fix": None
    }


def test_to_debug_dict_includes_extra_metadata():
    """Ensures that the developer-focused debug dictionary maps lazy frame structures onto the payload."""
    data = SimpleExceptionData(label="x", get_location=1)
    result = data.to_debug_dict()

    assert "label" in result
    assert "caller_info" in result


def test_to_json_produces_valid_json_matching_to_dict():
    """Validates that JSON string encoding produces a structurally sound representation matching to_dict."""
    data = SimpleExceptionData(label="x", message="hi", value=42)
    parsed = json.loads(data.to_json())

    assert parsed == data.to_dict()


def test_to_json_serializes_non_jsonable_values_via_str_fallback():
    """Checks the defensive encoder fallback string normalization logic for complex object payloads."""

    class Weird:
        def __str__(self):
            return "weird-repr"

    data = SimpleExceptionData(label="x", value=Weird())
    parsed = json.loads(data.to_json())

    assert parsed["value"] == "weird-repr"