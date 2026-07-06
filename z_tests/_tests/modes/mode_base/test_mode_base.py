"""
Tests for ModeBase — abstract behavior, default outcomes, and callable interface.
Fixed: Explicitly setting UNSET to avoid MagicMock auto-labels in output.
"""
import pytest
from abc import ABC
from unittest.mock import MagicMock
from simplibs.exception.modes.mode_base.ModeBase import ModeBase
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData
from simplibs.sentinels import UNSET


# -----------------------------------------------------------------------------
# Test Implementations
# -----------------------------------------------------------------------------

class MinimalMode(ModeBase):
    """Minimal implementation to verify default base behavior."""
    def _full_outcome(self, data: SimpleExceptionData) -> str:
        return "full_implemented"


@pytest.fixture
def minimal_mode():
    return MinimalMode()


@pytest.fixture
def sample_data():
    """
    Provides a Mock of SimpleExceptionData with controlled fields.
    Crucial: Unused fields are set to UNSET to prevent MagicMock artifacts in strings.
    """
    mock_data = MagicMock(spec=SimpleExceptionData)

    # Core identity
    mock_data.error_name = "TEST_ERROR"
    mock_data.message = "Simple message"

    # Clear out unused fields that PrintIntroLineMixin might try to render
    mock_data.value_label = UNSET
    mock_data.value = UNSET
    mock_data.expected = UNSET
    mock_data.problem = UNSET
    mock_data.context = UNSET
    mock_data.how_to_fix = UNSET

    # Mocked caller info property
    mock_data.caller_info = {
        "file": "test.py",
        "line": 10,
        "full_path": "/path/to/test.py",
        "function": "test_func"
    }

    return mock_data


# -----------------------------------------------------------------------------
# ABC and Structure
# -----------------------------------------------------------------------------

def test_mode_base_is_abstract():
    """ModeBase is an ABC and cannot be instantiated directly."""
    with pytest.raises(TypeError, match="instantiate abstract class"):
        ModeBase()


def test_mode_base_inheritance():
    """Ensure ModeBase inherits from necessary mixins and ABC."""
    from simplibs.exception.modes.mode_base._mixins.RenderMessage import RenderMessageMixin
    from simplibs.exception.modes.mode_base._mixins.PrintCallerInfo import PrintCallerInfoMixin

    assert issubclass(ModeBase, RenderMessageMixin)
    assert issubclass(ModeBase, PrintCallerInfoMixin)
    assert issubclass(ModeBase, ABC)


# -----------------------------------------------------------------------------
# Default Outcome Formats
# -----------------------------------------------------------------------------

def test_default_empty_outcome_format(minimal_mode, sample_data):
    """_empty_outcome should combine intro line and caller info using only data."""
    output = minimal_mode._empty_outcome(sample_data)

    # String should look like: "⚠️ TEST_ERROR: File: test.py | Line: 10 ..."
    assert "⚠️ TEST_ERROR" in output
    assert "File: test.py" in output
    assert "Line: 10" in output
    # Ensure no MagicMock leakage
    assert "MagicMock" not in output


def test_default_message_outcome_format(minimal_mode, sample_data):
    """_message_outcome should include the message and caller info on a new line."""
    output = minimal_mode._message_outcome(sample_data)

    assert "⚠️ TEST_ERROR: Simple message" in output
    assert "\nFile: test.py" in output
    assert "MagicMock" not in output


def test_outcome_with_missing_location(minimal_mode):
    """Outcomes must handle data with disabled/missing location gracefully."""
    data = MagicMock(spec=SimpleExceptionData)
    data.error_name = "SILENT"
    data.message = UNSET
    data.value_label = UNSET
    data.caller_info = None

    output = minimal_mode._empty_outcome(data)
    assert output == "⚠️ SILENT Location: Unknown"


# -----------------------------------------------------------------------------
# Dunder methods and Callability
# -----------------------------------------------------------------------------

def test_repr(minimal_mode):
    """Verify the string representation of the mode instance."""
    assert repr(minimal_mode) == "<MinimalMode mode>"


def test_call_proxies_to_render_message(minimal_mode, sample_data):
    """The __call__ method must act as a shortcut to render_message."""
    result = minimal_mode(sample_data, validate=False)

    assert "Simple message" in result
    assert "File: test.py" in result