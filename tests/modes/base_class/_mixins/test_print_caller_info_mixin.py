"""
Tests for PrintCallerInfoMixin — string output, dictionary output, and fallback behaviour.
"""
import pytest
from simplibs.exception.modes.base_class._mixins.PrintCallerInfo import PrintCallerInfoMixin


class MockMode(PrintCallerInfoMixin):
    pass


@pytest.fixture
def mode():
    return MockMode()


SAMPLE_CALLER_INFO = {
    "file": "test.py",
    "line": 10,
    "full_path": "/path/to/test.py",
    "function": "my_func"
}


# -----------------------------------------------------------------------------
# String output (as_dict=False)
# -----------------------------------------------------------------------------

def test_returns_string_with_correct_values(mode):
    """Must return a formatted string containing all caller info fields."""
    result = mode._print_caller_info(SAMPLE_CALLER_INFO, as_dict=False)
    assert isinstance(result, str)
    assert "File: test.py" in result
    assert "Line: 10" in result
    assert "Path: /path/to/test.py" in result
    assert "Function: my_func" in result


def test_as_dict_false_is_default(mode):
    """as_dict=False must be the default — calling without the parameter returns a string."""
    result = mode._print_caller_info(SAMPLE_CALLER_INFO)
    assert isinstance(result, str)


def test_none_returns_string_fallback(mode):
    """None caller_info must return 'Location: Unknown' string fallback."""
    assert mode._print_caller_info(None, as_dict=False) == "Location: Unknown"


def test_none_default_returns_string_fallback(mode):
    """None without as_dict parameter must also return string fallback."""
    assert mode._print_caller_info(None) == "Location: Unknown"


# -----------------------------------------------------------------------------
# Dict output (as_dict=True)
# -----------------------------------------------------------------------------

def test_returns_dict_with_correct_values(mode):
    """Must return a dict with correctly mapped keys and values."""
    result = mode._print_caller_info(SAMPLE_CALLER_INFO, as_dict=True)
    assert isinstance(result, dict)
    assert result["file"] == "test.py"
    assert result["line"] == 10
    assert result["path"] == "/path/to/test.py"
    assert result["func"] == "my_func"


def test_none_returns_dict_fallback(mode):
    """None caller_info with as_dict=True must return a safe fallback dict."""
    result = mode._print_caller_info(None, as_dict=True)
    assert isinstance(result, dict)
    assert result["file"] == "unknown"
    assert result["line"] == 0
    assert result["path"] == "unknown"
    assert result["func"] == "unknown"