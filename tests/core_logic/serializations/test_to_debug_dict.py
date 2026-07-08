from simplibs.exception._core_logic.serializations.to_debug_dict import to_debug_dict
from simplibs.exception.SimpleExceptionData import SimpleExceptionData
from simplibs.exception.SimpleException import SimpleException


def test_includes_all_standard_to_dict_fields():
    """Ensures that the debug snapshot implicitly carries over all core business-logic fields from the standard serialization."""
    data = SimpleExceptionData(label="my-label", message="hi")
    result = to_debug_dict(data)

    assert result["label"] == "my-label"
    assert result["message"] == "hi"


def test_caller_info_included_when_location_enabled():
    """Validates that enabling stack tracing successfully injects the dynamic caller filesystem frame metadata."""
    data = SimpleExceptionData(label="x", get_location=True)
    result = to_debug_dict(data)

    assert "caller_info" in result
    assert "function" in result["caller_info"]


def test_caller_info_omitted_when_location_disabled():
    """Confirms that when location tracking is explicitly disabled, the caller metadata block is entirely absent."""
    data = SimpleExceptionData(label="x", get_location=False)
    result = to_debug_dict(data)

    assert "caller_info" not in result


def test_intercepted_exception_included_when_set():
    """Verifies that an active, captured foreign exception footprint is explicitly embedded into the diagnostic dictionary."""
    data = SimpleExceptionData(label="x", intercepted_exception="ValueError: boom")
    result = to_debug_dict(data)

    assert result["intercepted_exception"] == "ValueError: boom"


def test_intercepted_exception_omitted_when_falsy():
    """Ensures that if no foreign exception was intercepted, the corresponding telemetry key is omitted."""
    data = SimpleExceptionData(label="x")
    result = to_debug_dict(data)

    assert "intercepted_exception" not in result


def test_rendered_message_omitted_on_plain_data_object():
    """
    Validates defensive attribute routing: querying a plain baseline data object
    (which lacks a text rendering pipeline) resolves gracefully without raising an AttributeError.
    """
    data = SimpleExceptionData(label="x")
    result = to_debug_dict(data)

    assert "rendered_message" not in result


def test_rendered_message_included_on_real_exception_instance():
    """Guarantees that a fully instantiated live exception dumps its final, user-facing terminal string block into the snapshot."""
    err = SimpleException("boom", label="x")
    result = to_debug_dict(err)

    assert "rendered_message" in result
    assert result["rendered_message"] == err.rendered_message


def test_unset_sentinels_are_filtered_out_via_underlying_composition():
    """
    Architectural Integration Case: Verifies that the underlying to_dict filtration
    mechanics pass through cleanly. Any attribute bound to the internal UNSET sentinel
    must be fully discarded from the final debug dictionary payload.
    """
    # 1. Instantiate with an explicit field omitted (resolves to UNSET)
    data = SimpleExceptionData(label="debug-filtration-test")
    result = to_debug_dict(data)

    # 2. Assert that fields untouched by the user do not spill sentinel tokens into telemetry
    assert "value" not in result