"""
Tests for LOG mode — empty outcome, message outcome, full outcome field order, and location handling.
"""
import pytest
from unittest.mock import MagicMock
from simplibs.exception.modes.LOG import LOG
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData
from simplibs.sentinels import UNSET

MOCK_CALLER_INFO = {
    "file": "app.py",
    "line": 42,
    "full_path": "path/app.py",
    "function": "func"
}


@pytest.fixture
def log_data():
    """Provides a Mock of SimpleExceptionData configured for LOG mode tests."""
    data = MagicMock(spec=SimpleExceptionData)
    data.error_name = "LOG_TEST"
    data.message = UNSET
    data.value_label = UNSET
    data.value = UNSET
    data.expected = UNSET
    data.problem = UNSET
    data.context = UNSET
    data.how_to_fix = UNSET
    data.caller_info = MOCK_CALLER_INFO
    return data


# -----------------------------------------------------------------------------
# _empty_outcome
# -----------------------------------------------------------------------------

def test_empty_outcome_contains_error_and_location(log_data):
    """An empty call must contain error= and file=/line=."""
    # Act
    output = LOG(log_data, validate=False)

    # Assert
    assert "error=LOG_TEST" in output
    assert "file='app.py'" in output
    assert "line=42" in output
    assert "message=" not in output


def test_empty_outcome_uses_fallback_when_caller_info_missing(log_data):
    """If caller_info is missing/None, _empty_outcome must use fallback values via mixin logic."""
    log_data.caller_info = None

    output = LOG(log_data, validate=False)

    assert "error=LOG_TEST" in output
    assert "file='unknown'" in output
    assert "line=0" in output


# -----------------------------------------------------------------------------
# _message_outcome
# -----------------------------------------------------------------------------

def test_message_outcome_contains_message_and_location(log_data):
    """A message-only call must contain message= and the location."""
    log_data.message = "Log message"

    output = LOG(log_data, validate=False)

    assert "error=LOG_TEST" in output
    assert "message='Log message'" in output
    assert "file='app.py'" in output
    assert "line=42" in output


# -----------------------------------------------------------------------------
# _full_outcome — field order
# -----------------------------------------------------------------------------

def test_full_outcome_field_order(log_data):
    """Fields must appear in order: error, message, value_label, value, expected, problem, how_to_fix."""
    log_data.error_name = "ORDER_TEST"
    log_data.message = "a message"
    log_data.value_label = "parameter"
    log_data.value = "complex"
    log_data.expected = "simple"
    log_data.problem = "wrong type"
    log_data.how_to_fix = ("Fix it",)
    # Location is set via fixture MOCK_CALLER_INFO

    output = LOG(log_data, validate=False)

    # Dictionary to store found positions
    positions = {
        "error":       output.index("error="),
        "message":     output.index("message="),
        "value_label": output.index("value_label="),
        "value":       output.index("value="),
        "expected":    output.index("expected="),
        "problem":     output.index("problem="),
        "file":        output.index("file="),
        "how_to_fix":  output.index("how_to_fix="),
    }

    # Assert correct sequential order
    keys = ["error", "message", "value_label", "value", "expected", "problem", "file", "how_to_fix"]
    for i in range(len(keys) - 1):
        assert positions[keys[i]] < positions[keys[i+1]], f"{keys[i]} should be before {keys[i+1]}"


def test_full_outcome_how_to_fix_joined_with_separator(log_data):
    """A how_to_fix tuple must be joined with ' | ' and wrapped in quotes."""
    log_data.how_to_fix = ("A", "B")
    log_data.caller_info = None # Keep it simple

    output = LOG(log_data, validate=False)

    assert "how_to_fix='A | B'" in output


def test_full_outcome_file_and_line_hidden_when_no_caller_info(log_data):
    """In full_outcome, file= and line= must be completely omitted if caller_info is None."""
    log_data.problem = "a problem"
    log_data.caller_info = None

    output = LOG(log_data, validate=False)

    assert "file=" not in output
    assert "line=" not in output


def test_full_outcome_no_none_in_output(log_data):
    """The output must not contain the string 'None' anywhere — all UNSET/None fields are skipped."""
    log_data.problem = "Only problem"
    # Even with missing location
    log_data.caller_info = None

    output = LOG(log_data, validate=False)

    assert "None" not in output
    assert output == "error=LOG_TEST problem='Only problem'"