"""
Tests for ONELINE mode — single-line guarantee, field content, field order, and location handling.
"""
import pytest
from unittest.mock import patch
from simplibs.exception.modes.ONELINE import ONELINE
from simplibs.exception.base.data.SimpleExceptionData import SimpleExceptionData

MOCK_CALLER_INFO = {
    "file": "t.py",
    "line": 1,
    "full_path": "path/t.py",
    "function": "func"
}


# -----------------------------------------------------------------------------
# Critical properties
# -----------------------------------------------------------------------------

def test_oneline_is_single_line():
    """The output must never contain a newline character."""
    data = SimpleExceptionData(
        error_name="LONG_ERROR",
        message="This is a long message",
        problem="Some problem",
    )
    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=MOCK_CALLER_INFO):
        output = ONELINE(data, validate=False)

    assert "\n" not in output.strip()


def test_no_none_in_output():
    """The output must not contain the string 'None' anywhere — UNSET fields are skipped."""
    data = SimpleExceptionData(problem="Only problem")
    data._get_location = False

    output = ONELINE(data, validate=False)

    assert "None" not in output


def test_no_empty_separators():
    """UNSET fields must not leave empty pipes '||' in the output."""
    data = SimpleExceptionData(error_name="FILTER", expected="Valid string")
    data._get_location = False

    output = ONELINE(data, validate=False)

    assert "||" not in output
    assert not output.strip().endswith("|")


# -----------------------------------------------------------------------------
# _empty_outcome
# -----------------------------------------------------------------------------

def test_empty_outcome_with_caller_info():
    """An empty call with caller_info must contain the error name and location."""
    data = SimpleExceptionData(error_name="EMPTY")

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=MOCK_CALLER_INFO):
        output = ONELINE(data, validate=False)

    assert output.startswith("⚠️ EMPTY |")
    assert "File: t.py" in output
    assert "Line: 1" in output


def test_empty_outcome_without_caller_info():
    """An empty call without location must contain 'Location: Unknown'."""
    data = SimpleExceptionData(error_name="EMPTY")
    data._get_location = False

    output = ONELINE(data, validate=False)

    assert output.startswith("⚠️ EMPTY |")
    assert "Location: Unknown" in output


# -----------------------------------------------------------------------------
# _message_outcome
# -----------------------------------------------------------------------------

def test_message_outcome_format():
    """A message-only call must have the correct format."""
    data = SimpleExceptionData(error_name="MSG", message="something went wrong")
    data._get_location = False

    output = ONELINE(data, validate=False)

    assert output.startswith("⚠️ MSG: something went wrong |")


# -----------------------------------------------------------------------------
# _full_outcome
# -----------------------------------------------------------------------------

def test_full_outcome_contains_all_fields():
    """The full output must contain all provided fields."""
    data = SimpleExceptionData(
        error_name="FULL",
        value_label="parameter",
        message="free-form message",
        expected="str",
        value=42,
        problem="wrong type",
        context="inside loop ID=5",
    )
    data._get_location = False

    output = ONELINE(data, validate=False)

    assert "⚠️ FULL" in output
    assert "parameter" in output
    assert "Message: free-form message" in output
    assert "Expected: str" in output
    assert "Got: 42 (int)" in output
    assert "Problem: wrong type" in output
    assert "Context: inside loop ID=5" in output


def test_full_outcome_field_order():
    """Fields must appear in the order defined in __DOC__."""
    data = SimpleExceptionData(
        error_name="ORDER",
        value_label="parameter",
        message="a message",
        expected="str",
        value=42,
        problem="wrong type",
        context="context",
    )
    data._get_location = False

    output = ONELINE(data, validate=False)

    assert output.index("parameter") < output.index("Message:")
    assert output.index("Message:") < output.index("Expected:")
    assert output.index("Expected:") < output.index("Got:")
    assert output.index("Got:") < output.index("Problem:")
    assert output.index("Problem:") < output.index("Context:")


def test_full_outcome_no_caller_info_when_disabled():
    """If caller_info is None, the location must not appear in the full output."""
    data = SimpleExceptionData(error_name="NO_LOC", problem="a problem")
    data._get_location = False

    output = ONELINE(data, validate=False)

    assert "File:" not in output
    assert "Line:" not in output


def test_full_outcome_how_to_fix_is_not_shown():
    """how_to_fix is intentionally not displayed in ONELINE mode."""
    data = SimpleExceptionData(
        error_name="TEST",
        how_to_fix=("Hidden", "Secret"),
        problem="some problem",
    )
    data._get_location = False

    output = ONELINE(data, validate=False)

    assert "Hidden" not in output
    assert "Secret" not in output


def test_full_outcome_context_appears_after_problem():
    """context must appear after problem in the output."""
    data = SimpleExceptionData(
        error_name="CTX",
        problem="an error",
        context="processing batch ID=42",
    )
    data._get_location = False

    output = ONELINE(data, validate=False)

    assert "Context: processing batch ID=42" in output
    assert output.index("Problem:") < output.index("Context:")