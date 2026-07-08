from simplibs.exception._core_logic.serializations.to_dict import to_dict
from simplibs.exception.SimpleExceptionData import SimpleExceptionData


def test_unset_value_is_omitted():
    """Ensures that fields holding the internal UNSET sentinel token are dynamically omitted from the serialized dictionary."""
    data = SimpleExceptionData(label="label-only")
    result = to_dict(data)

    assert "value" not in result


def test_set_fields_are_included():
    """Validates that all explicitly populated business-logic metadata fields are accurately mapped into the output payload."""
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
    """
    Verifies boundary sentinel distinction: fields defaulting to explicit None states
    must be preserved inside the output, confirming they are not mixed up with UNSET logic.
    """
    data = SimpleExceptionData()
    result = to_dict(data)

    assert "label" in result
    assert result["label"] is None


def test_internal_location_metadata_is_not_included():
    """
    Architectural Contract: Guarantees that internal runtime controls, layout configurations,
    and computed location metadata frames never leak into the public serialized dictionary.
    """
    data = SimpleExceptionData(label="x", get_location=True)
    result = to_dict(data)

    assert "get_location" not in result
    assert "skip_locations" not in result
    assert "caller_info" not in result
    assert "oneline" not in result


def test_dictionary_mapping_completeness_guard():
    """
    Architectural Guard Rail: Verifies that the explicit mapping inside to_dict remains
    fully complete. If a developer registers a new public data field in SimpleExceptionData,
    this test triggers a failure until the serialization candidate dictionary is updated.
    """
    from simplibs.sentinels import UNSET

    # 1. Inspect all public annotations on the data blueprint class
    all_public_annotations = {
        name for name, typ in SimpleExceptionData.__annotations__.items()
        if not name.startswith("_")
    }

    # 2. Define explicit configuration parameters that are intentionally hidden from to_dict
    ignored_config_fields = {
        "oneline",
        "exception",
        "intercepted_exception",
        "get_location",
        "skip_locations",
    }

    # 3. Derive the strict expected business-logic data contract fields
    expected_data_fields = all_public_annotations - ignored_config_fields

    # 4. Instantiate a comprehensive mock containing non-UNSET data for every single field
    kwargs = {field: "mock-value" for field in all_public_annotations}
    data = SimpleExceptionData(**kwargs)

    # 5. Execute serialization pass
    result = to_dict(data)

    # 6. Assert that every business data field successfully serialized into the dictionary
    assert set(result.keys()) == expected_data_fields