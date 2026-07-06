from simplibs.exception.modes.printers.hepl_info_multiline.print_intercepted_exception import (
    print_intercepted_exception,
)


def test_none_returns_none():
    assert print_intercepted_exception(None) is None


def test_non_exception_value_returns_none():
    assert print_intercepted_exception("not an exception") is None


def test_exception_class_instead_of_instance_returns_none():
    # A class is not an *instance* of Exception, so this is intentionally
    # rejected too.
    assert print_intercepted_exception(ValueError) is None


def test_standard_mode_with_message():
    err = ValueError("bad value")
    result = print_intercepted_exception(err)
    assert result == "Intercepted exception (ValueError):\n    bad value"


def test_standard_mode_without_message():
    err = ValueError()
    result = print_intercepted_exception(err)
    assert result == "Intercepted exception (ValueError)"


def test_custom_prefix_is_respected():
    err = ValueError("bad value")
    result = print_intercepted_exception(err, prefix="Caused by")
    assert result == "Caused by (ValueError):\n    bad value"


def test_oneline_mode_flattens_multiline_message():
    err = ValueError("line one\nline two")
    result = print_intercepted_exception(err, _oneline=True)
    assert result == "Intercepted exception (ValueError): line one line two"


def test_oneline_mode_without_message():
    err = ValueError()
    result = print_intercepted_exception(err, _oneline=True)
    assert result == "Intercepted exception (ValueError)"


def test_log_mode_only_includes_class_name():
    err = ValueError("bad value")
    result = print_intercepted_exception(err, _log_mode=True)
    assert result == "intercepted_exception='ValueError'"
