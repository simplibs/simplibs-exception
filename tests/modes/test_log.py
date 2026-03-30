"""
Tests for LOG mode — empty outcome, message outcome, full outcome field order, and location handling.
"""
import pytest
from unittest.mock import patch
from simplibs.exception.modes.LOG import LOG
from simplibs.exception.core.data.SimpleExceptionData import SimpleExceptionData

MOCK_CALLER_INFO = {
    "file": "app.py",
    "line": 42,
    "full_path": "path/app.py",
    "function": "func"
}


# -----------------------------------------------------------------------------
# _empty_outcome
# -----------------------------------------------------------------------------

def test_empty_outcome_contains_error_and_location(mode=LOG):
    """An empty call must contain error= and file=/line=."""
    data = SimpleExceptionData(error_name="LOG_TEST")

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=MOCK_CALLER_INFO):
        output = LOG(data, validate=False)

    assert "error=LOG_TEST" in output
    assert "file='app.py'" in output
    assert "line=42" in output
    assert "message=" not in output


def test_empty_outcome_uses_fallback_when_caller_info_none():
    """If extract_caller_info returns None, _empty_outcome must use fallback values."""
    data = SimpleExceptionData(error_name="LOG_TEST")

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=None):
        output = LOG(data, validate=False)

    assert "error=LOG_TEST" in output
    assert "file='unknown'" in output
    assert "line=0" in output


def test_empty_outcome_without_location_when_disabled():
    """If _get_location=False, _empty_outcome must use the fallback — location is not resolved."""
    data = SimpleExceptionData(error_name="LOG_TEST")
    data._get_location = False

    output = LOG(data, validate=False)

    assert "error=LOG_TEST" in output
    assert "file='unknown'" in output
    assert "line=0" in output


# -----------------------------------------------------------------------------
# _message_outcome
# -----------------------------------------------------------------------------

def test_message_outcome_contains_message_and_location():
    """A message-only call must contain message= and the location."""
    data = SimpleExceptionData(error_name="LOG_TEST", message="Log message")

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=MOCK_CALLER_INFO):
        output = LOG(data, validate=False)

    assert "error=LOG_TEST" in output
    assert "message='Log message'" in output
    assert "file='app.py'" in output
    assert "line=42" in output


# -----------------------------------------------------------------------------
# _full_outcome — field order
# -----------------------------------------------------------------------------

def test_full_outcome_field_order():
    """Fields must appear in order: error, message, value_label, value, expected, problem, how_to_fix."""
    data = SimpleExceptionData(
        error_name="ORDER_TEST",
        message="a message",
        value_label="parameter",
        value="complex",
        expected="simple",
        problem="wrong type",
        how_to_fix=("Fix it",)
    )
    data._get_location = False

    output = LOG(data, validate=False)

    positions = {
        "error":       output.index("error="),
        "message":     output.index("message="),
        "value_label": output.index("value_label="),
        "value":       output.index("value="),
        "expected":    output.index("expected="),
        "problem":     output.index("problem="),
        "how_to_fix":  output.index("how_to_fix="),
    }
    assert positions["error"] < positions["message"]
    assert positions["message"] < positions["value_label"]
    assert positions["value_label"] < positions["value"]
    assert positions["value"] < positions["expected"]
    assert positions["expected"] < positions["problem"]
    assert positions["problem"] < positions["how_to_fix"]


def test_full_outcome_message_appears_before_problem():
    """message= must appear before problem= in the full output."""
    data = SimpleExceptionData(
        error_name="MSG_TEST",
        message="free-form message",
        problem="some problem"
    )
    data._get_location = False

    output = LOG(data, validate=False)

    assert "message='free-form message'" in output
    assert output.index("message=") < output.index("problem=")


def test_full_outcome_how_to_fix_joined_with_separator():
    """A how_to_fix tuple must be joined with ' | ' and wrapped in quotes."""
    data = SimpleExceptionData(error_name="FIX", how_to_fix=("A", "B"))
    data._get_location = False

    output = LOG(data, validate=False)

    assert "how_to_fix='A | B'" in output


def test_full_outcome_file_and_line_hidden_when_no_caller_info():
    """If caller_info is None, file= and line= must not appear in the full output."""
    data = SimpleExceptionData(error_name="NO_LOC", problem="a problem")
    data._get_location = False

    output = LOG(data, validate=False)

    assert "file=" not in output
    assert "line=" not in output


def test_full_outcome_no_none_in_output():
    """The output must not contain the string 'None' anywhere — all UNSET fields are skipped."""
    data = SimpleExceptionData(problem="Only problem")
    data._get_location = False

    output = LOG(data, validate=False)

    assert "None" not in output