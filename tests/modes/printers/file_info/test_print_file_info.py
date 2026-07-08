from simplibs.exception.modes.printers.file_info.print_file_info import (
    print_file_info,
)


def test_none_returns_none():
    """Confirms that passing a None dictionary context gracefully yields None, indicating the row should be skipped."""
    assert print_file_info(None) is None


def test_empty_dict_returns_none():
    """Ensures that an empty dictionary payload is treated as omitted metadata, skipping row compilation."""
    assert print_file_info({}) is None


def test_dynamic_frame_file_is_formatted_normally():
    """
    Architectural Contract: Verifies that the printer does not perform hidden business logic filtering.
    If an internal dynamic fallback string (like <string>) reaches this layer, the engine must format it objectively.
    """
    caller_info = {
        "file": "<string>",
        "path": "<string>",
        "line": 1,
        "function": "f"
    }
    result = print_file_info(caller_info)

    assert result == "File info: <string> | line: 1 | function: f"


def test_standard_mode_format():
    """Validates the standard human-readable presentation format, utilizing vertical pipes as distinct structural dividers."""
    caller_info = {
        "file": "my_module.py",
        "path": "/some/path/my_module.py",
        "line": 42,
        "function": "my_function",
    }
    result = print_file_info(caller_info)
    assert result == "File info: my_module.py | line: 42 | function: my_function"


def test_custom_prefix_is_respected():
    """Verifies layout flexibility by ensuring the file metadata printer correctly renders a customized prefix marker."""
    caller_info = {
        "file": "my_module.py",
        "path": "/some/path/my_module.py",
        "line": 42,
        "function": "my_function",
    }
    result = print_file_info(caller_info, prefix="FILE: ")
    assert result == "FILE: my_module.py | line: 42 | function: my_function"


def test_log_mode_format():
    """
    Verifies Log Mode layout consistency: string properties (file, function) must use safe repr quotes,
    while the guaranteed integer line property emits cleanly as an unquoted token.
    """
    caller_info = {
        "file": "my_module.py",
        "path": "/some/path/my_module.py",
        "line": 42,
        "function": "my_function",
    }
    result = print_file_info(caller_info, _log_mode=True)
    assert result == "file='my_module.py' line=42 function='my_function'"


