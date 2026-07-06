from simplibs.exception._core_logic.serializations.to_debug_dict import to_debug_dict
from simplibs.exception.SimpleExceptionData import SimpleExceptionData
from simplibs.exception.SimpleException import SimpleException


def test_includes_all_standard_to_dict_fields():
    data = SimpleExceptionData(label="my-label", message="hi")
    result = to_debug_dict(data)

    assert result["label"] == "my-label"
    assert result["message"] == "hi"


def test_caller_info_included_when_location_enabled():
    data = SimpleExceptionData(label="x", get_location=True)
    result = to_debug_dict(data)

    assert "caller_info" in result
    assert "function" in result["caller_info"]


def test_caller_info_omitted_when_location_disabled():
    data = SimpleExceptionData(label="x", get_location=False)
    result = to_debug_dict(data)

    assert "caller_info" not in result


def test_intercepted_exception_included_when_set():
    data = SimpleExceptionData(label="x", intercepted_exception="ValueError: boom")
    result = to_debug_dict(data)

    assert result["intercepted_exception"] == "ValueError: boom"


def test_intercepted_exception_omitted_when_falsy():
    data = SimpleExceptionData(label="x")
    result = to_debug_dict(data)

    assert "intercepted_exception" not in result


def test_rendered_message_omitted_on_plain_data_object():
    # SimpleExceptionData itself never sets `rendered_message`.
    data = SimpleExceptionData(label="x")
    result = to_debug_dict(data)

    assert "rendered_message" not in result


def test_rendered_message_included_on_real_exception_instance():
    err = SimpleException("boom", label="x")
    result = to_debug_dict(err)

    assert "rendered_message" in result
    assert result["rendered_message"] == err.rendered_message
