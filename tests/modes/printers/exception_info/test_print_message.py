from simplibs.exception.modes.printers.exception_info.print_message import (
    print_message,
)


def test_none_returns_none():
    assert print_message(None) is None


def test_empty_string_returns_none():
    assert print_message("") is None


def test_standard_mode_uses_default_prefix():
    assert print_message("hello world") == "Message:   hello world"


def test_standard_mode_uses_custom_prefix():
    assert print_message("hello world", prefix="MSG: ") == "MSG: hello world"


def test_log_mode_format():
    assert print_message("hello world", _log_mode=True) == "message='hello world'"
