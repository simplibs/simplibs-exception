from simplibs.exception.modes.printers.file_info.print_file_path import (
    print_file_path,
)


def test_none_returns_none():
    """Confirms that passing a None context gracefully yields None, indicating the row should be skipped."""
    assert print_file_path(None) is None


def test_empty_dict_returns_none():
    """Ensures that an empty dictionary payload evaluates to an empty context and returns None."""
    assert print_file_path({}) is None


def test_dynamic_frame_path_is_formatted_normally():
    """
    Architectural Contract: Verifies that the printer does not perform hidden business logic filtering on paths.
    If an internal dynamic fallback string (like <string>) reaches this layer, the engine must format it objectively.
    """
    caller_info = {
        "file": "<string>",
        "path": "<string>",
        "line": 1,
        "function": "f"
    }
    result = print_file_path(caller_info)

    assert result == "File path: <string>"


def test_standard_mode_format():
    """Validates the standard human-readable path layout generation using the default prefix."""
    caller_info = {
        "file": "my_module.py",
        "path": "/some/path/my_module.py",
        "line": 42,
        "function": "my_function",
    }
    result = print_file_path(caller_info)
    assert result == "File path: /some/path/my_module.py"


def test_custom_prefix_is_respected():
    """Ensures that an explicitly provided custom prefix completely overrides the standard default."""
    caller_info = {
        "file": "my_module.py",
        "path": "/some/path/my_module.py",
        "line": 42,
        "function": "my_function",
    }
    result = print_file_path(caller_info, prefix="PATH: ")
    assert result == "PATH: /some/path/my_module.py"


def test_log_mode_format():
    """Verifies the structured, machine-scannable attribute format generated when log mode is active, enforcing safe repr encapsulation."""
    caller_info = {
        "file": "my_module.py",
        "path": "/some/path/my_module.py",
        "line": 42,
        "function": "my_function",
    }
    result = print_file_path(caller_info, _log_mode=True)
    assert result == "path='/some/path/my_module.py'"


