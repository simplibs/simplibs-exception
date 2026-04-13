"""
Tests for PrintCallerInfoMixin — string output, dictionary output, and fallback behaviour.
Integrates with SimpleExceptionData.caller_info property.
"""
import pytest
from unittest.mock import MagicMock
from simplibs.exception.modes.mode_base._mixins.PrintCallerInfo import PrintCallerInfoMixin
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData


class MockMode(PrintCallerInfoMixin):
    """Mock class to host the mixin for testing."""
    pass


@pytest.fixture
def mode():
    return MockMode()


@pytest.fixture
def sample_data():
    """Provides a SimpleExceptionData mock with predefined caller_info."""
    data = MagicMock(spec=SimpleExceptionData)
    data.caller_info = {
        "file": "test.py",
        "line": 42,
        "full_path": "/home/user/test.py",
        "function": "validate"
    }
    return data


@pytest.fixture
def empty_data():
    """Provides a SimpleExceptionData mock with missing caller_info."""
    data = MagicMock(spec=SimpleExceptionData)
    data.caller_info = None
    return data


# -----------------------------------------------------------------------------
# String output (as_dict=False)
# -----------------------------------------------------------------------------

def test_returns_formatted_string(mode, sample_data):
    """Must return a formatted string with pipe-separated location details."""
    result = mode._print_caller_info(sample_data, as_dict=False)

    assert isinstance(result, str)
    assert "File: test.py" in result
    assert "Line: 42" in result
    assert "Path: /home/user/test.py" in result
    assert "Function: validate" in result
    assert result.count(" | ") == 3


def test_as_dict_false_is_default(mode, sample_data):
    """Calling without as_dict must return a string by default."""
    result = mode._print_caller_info(sample_data)
    assert isinstance(result, str)
    assert "File: test.py" in result


def test_missing_info_returns_string_fallback(mode, empty_data):
    """When caller_info is None, it must return a safe 'Unknown' string."""
    result = mode._print_caller_info(empty_data, as_dict=False)
    assert result == "Location: Unknown"


# -----------------------------------------------------------------------------
# Dictionary output (as_dict=True)
# -----------------------------------------------------------------------------

def test_returns_mapped_dictionary(mode, sample_data):
    """Must return a dictionary with keys mapped for LOG mode processing."""
    result = mode._print_caller_info(sample_data, as_dict=True)

    assert isinstance(result, dict)
    assert result["file"] == "test.py"
    assert result["line"] == 42
    assert result["path"] == "/home/user/test.py"
    assert result["func"] == "validate"


def test_missing_info_returns_dict_fallback(mode, empty_data):
    """When caller_info is None, it must return a dictionary with 'unknown' placeholders."""
    result = mode._print_caller_info(empty_data, as_dict=True)

    assert isinstance(result, dict)
    assert result["file"] == "unknown"
    assert result["line"] == 0
    assert result["path"] == "unknown"
    assert result["func"] == "unknown"


# -----------------------------------------------------------------------------
# Data Access
# -----------------------------------------------------------------------------

def test_accesses_data_caller_info_property(mode, sample_data):
    """The mixin must access the 'caller_info' property of the data object."""
    mode._print_caller_info(sample_data)
    # Verify the property was accessed at least once
    assert sample_data.caller_info is not None