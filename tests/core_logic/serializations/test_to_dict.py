from simplibs.exception._core_logic.serializations.to_dict import to_dict
from simplibs.exception.SimpleExceptionData import SimpleExceptionData


def test_unset_value_is_omitted():
    data = SimpleExceptionData(label="label-only")
    result = to_dict(data)

    assert "value" not in result


def test_set_fields_are_included():
    data = SimpleExceptionData(
        label="my-label",
        message="my-message",
        expected="expected-thing",
        value=42,
        problem="something failed",
        context="extra context",
        how_to_fix="do this instead",
    )
    result = to_dict(data)

    assert result["label"] == "my-label"
    assert result["message"] == "my-message"
    assert result["expected"] == "expected-thing"
    assert result["value"] == 42
    assert result["problem"] == "something failed"
    assert result["context"] == "extra context"
    assert result["how_to_fix"] == "do this instead"
    assert result["error_name"] == "ERROR"


def test_none_fields_are_kept_not_treated_as_unset():
    # label defaults to None, not UNSET — None values should NOT be filtered out.
    data = SimpleExceptionData()
    result = to_dict(data)

    assert "label" in result
    assert result["label"] is None


def test_internal_location_metadata_is_not_included():
    data = SimpleExceptionData(label="x", get_location=True)
    result = to_dict(data)

    assert "get_location" not in result
    assert "skip_locations" not in result
    assert "caller_info" not in result
    assert "oneline" not in result
