from simplibs.exception.modes.printers.file_info.print_file_info import (
    print_file_info,
)


def test_none_returns_none():
    assert print_file_info(None) is None


def test_empty_dict_returns_none():
    assert print_file_info({}) is None


def test_dynamic_frame_file_is_formatted_normally():
    """
    Verifies that the printer does not perform business logic filtering.
    If a dynamic frame layout (like <string>) escapes upstream processing
    or serves as a fallback, the printer must format it objectively.
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
    caller_info = {
        "file": "my_module.py",
        "path": "/some/path/my_module.py",
        "line": 42,
        "function": "my_function",
    }
    result = print_file_info(caller_info)
    assert result == "File info: my_module.py | line: 42 | function: my_function"


def test_custom_prefix_is_respected():
    caller_info = {
        "file": "my_module.py",
        "path": "/some/path/my_module.py",
        "line": 42,
        "function": "my_function",
    }
    result = print_file_info(caller_info, prefix="FILE: ")
    assert result == "FILE: my_module.py | line: 42 | function: my_function"


def test_log_mode_format():
    caller_info = {
        "file": "my_module.py",
        "path": "/some/path/my_module.py",
        "line": 42,
        "function": "my_function",
    }
    result = print_file_info(caller_info, _log_mode=True)
    assert result == "file='my_module.py' line=42 function='my_function'"
