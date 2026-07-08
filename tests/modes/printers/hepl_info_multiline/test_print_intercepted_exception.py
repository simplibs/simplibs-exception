from simplibs.exception.modes.printers.hepl_info_multiline.print_intercepted_exception import (
    print_intercepted_exception,
)


def test_none_returns_none():
    """Confirms that passing a None value gracefully yields None, indicating the field should be skipped in the layout."""
    assert print_intercepted_exception(None) is None


def test_non_exception_value_returns_none():
    """Ensures that basic primitive types or un-thrown objects fail the type guard and return None."""
    assert print_intercepted_exception("not an exception") is None


def test_exception_class_instead_of_instance_returns_none():
    """
    Architectural Contract: Enforces that an uninstantiated Exception blueprint class
    fails the strict instance check, protecting downstream renderers from type failures.
    """
    assert print_intercepted_exception(ValueError) is None


def test_standard_mode_with_message():
    """Validates standard human-friendly breakdown format, indenting third-party messages below the prefix line."""
    err = ValueError("bad value")
    result = print_intercepted_exception(err)
    assert result == "Intercepted exception (ValueError):\n    bad value"


def test_standard_mode_without_message():
    """Ensures that exceptions without message payloads omit the trailing colon and whitespace padding gracefully."""
    err = ValueError()
    result = print_intercepted_exception(err)
    assert result == "Intercepted exception (ValueError)"


def test_custom_prefix_is_respected():
    """Verifies layout flexibility by ensuring the intercept printer dynamically applies a customized prefix marker."""
    err = ValueError("bad value")
    result = print_intercepted_exception(err, prefix="Caused by")
    assert result == "Caused by (ValueError):\n    bad value"


def test_oneline_mode_flattens_multiline_message():
    """
    Verifies Horizontal Row Integrity: multi-line messages produced by third-party errors
    must collapse into a flat space-separated layout stream.
    """
    err = ValueError("line one\nline two")
    result = print_intercepted_exception(err, _oneline=True)
    assert result == "Intercepted exception (ValueError): line one line two"


def test_oneline_mode_without_message():
    """Ensures that Oneline Mode without an active message payload produces a clean, space-restricted format block."""
    err = ValueError()
    result = print_intercepted_exception(err, _oneline=True)
    assert result == "Intercepted exception (ValueError)"


def test_log_mode_only_includes_class_name():
    """
    Verifies Log Mode behavior: the output must capture only the clean python class name
    token using repr, discarding volatile dynamic message bodies for telemetry row safety.
    """
    err = ValueError("bad value")
    result = print_intercepted_exception(err, _log_mode=True)
    assert result == "intercepted_exception='ValueError'"


