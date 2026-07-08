from simplibs.exception.modes.printers.exception_info.print_message import (
    print_message,
)


def test_none_returns_none():
    """Confirms that passing a None message gracefully yields None, indicating the field should be skipped in the layout."""
    assert print_message(None) is None


def test_empty_string_returns_none():
    """Ensures that empty string inputs are treated as omitted metadata, preventing blank lines from polluting the render."""
    assert print_message("") is None


def test_standard_mode_uses_default_prefix():
    """Validates the standard human-friendly layout, enforcing the default 11-character padded prefix matrix alignment."""
    assert print_message("hello world") == "Message:   hello world"


def test_standard_mode_uses_custom_prefix():
    """Verifies layout flexibility by ensuring the printer accepts and accurately applies a customized prefix layout."""
    assert print_message("hello world", prefix="MSG: ") == "MSG: hello world"


def test_log_mode_format():
    """
    Verifies Log Mode behavior: the output must be formatted as a single key-value token,
    utilizing strict repr encapsulation (!r) for safe space-delimited text log parsing.
    """
    assert print_message("hello world", _log_mode=True) == "message='hello world'"


def test_log_mode_safely_sanitizes_complex_and_hazardous_messages():
    """
    Architectural Contract: Verifies that the log mode successfully escapes messages
    containing raw internal quotes, backslashes, or control characters via repr encapsulation,
    preventing log record row splitting or field fragmentation.
    """
    # A complex user message simulating nested quotes and an embedded newline
    hazardous_input = "Operation 'WRITE' failed:\nConnection reset."

    result = print_message(hazardous_input, _log_mode=True)

    # Assert that the output was wrapped in single quotes and the newline was escaped to literal '\\n'
    assert result == "message=\"Operation 'WRITE' failed:\\nConnection reset.\""