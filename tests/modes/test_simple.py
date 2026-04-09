"""
Tests for SIMPLE mode — no decorative lines, field content, field order, and parity with PRETTY.
"""
import pytest
from unittest.mock import patch
from simplibs.exception.modes.SIMPLE import SIMPLE
from simplibs.exception.modes.PRETTY import PRETTY
from simplibs.exception.base.data.SimpleExceptionData import SimpleExceptionData

MOCK_CALLER_INFO = {
    "file": "test.py",
    "line": 1,
    "full_path": "path/test.py",
    "function": "func"
}


# -----------------------------------------------------------------------------
# Critical properties
# -----------------------------------------------------------------------------

def test_no_decorative_lines_in_any_output():
    """SIMPLE must never contain decorative lines ═ or ─."""
    data = SimpleExceptionData(
        error_name="FULL_SIMPLE",
        problem="Network timeout",
        how_to_fix=("Check connection",)
    )
    data._get_location = False

    output = SIMPLE(data, validate=False)

    assert "═" not in output
    assert "─" not in output


def test_no_none_in_output():
    """The output must not contain the string 'None' anywhere — UNSET fields are skipped."""
    data = SimpleExceptionData(problem="Only problem")
    data._get_location = False

    output = SIMPLE(data, validate=False)

    assert "None" not in output


# -----------------------------------------------------------------------------
# _empty_outcome (inherited from ModeBase)
# -----------------------------------------------------------------------------

def test_empty_outcome_starts_with_error_name():
    """The empty output must start with the error name without any decoration."""
    data = SimpleExceptionData(error_name="SIMPLE_TEST")
    data._get_location = False

    output = SIMPLE(data, validate=False)

    assert output.startswith("⚠️ SIMPLE_TEST:")


def test_empty_outcome_with_caller_info():
    """Caller info must be included in the empty output when available."""
    data = SimpleExceptionData(error_name="SIMPLE_TEST")

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=MOCK_CALLER_INFO):
        output = SIMPLE(data, validate=False)

    assert "File: test.py" in output
    assert "Line: 1" in output


# -----------------------------------------------------------------------------
# _full_outcome
# -----------------------------------------------------------------------------

def test_full_outcome_contains_all_fields():
    """The full output must contain all provided fields."""
    data = SimpleExceptionData(
        error_name="FULL_SIMPLE",
        message="a message",
        expected="str",
        value=42,
        problem="Network timeout",
        context="inside a loop",
        how_to_fix=("Check connection",),
    )
    data._get_location = False

    output = SIMPLE(data, validate=False)

    assert "⚠️ FULL_SIMPLE:" in output
    assert "Message:   a message" in output
    assert "Expected:  str" in output
    assert "Got:       42 (int)" in output
    assert "Problem:   Network timeout" in output
    assert "Context:   inside a loop" in output
    assert "How to fix:" in output
    assert "• Check connection" in output


def test_full_outcome_field_order():
    """Fields must appear in order: Message, Expected, Got, Problem, Context."""
    data = SimpleExceptionData(
        error_name="ORDER",
        message="a message",
        expected="str",
        value=42,
        problem="wrong type",
        context="context",
    )
    data._get_location = False

    output = SIMPLE(data, validate=False)

    assert output.index("Message:") < output.index("Expected:")
    assert output.index("Expected:") < output.index("Got:")
    assert output.index("Got:") < output.index("Problem:")
    assert output.index("Problem:") < output.index("Context:")


def test_full_outcome_with_caller_info():
    """The File info line must be shown when caller_info is available."""
    data = SimpleExceptionData(problem="Some problem")

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=MOCK_CALLER_INFO):
        output = SIMPLE(data, validate=False)

    assert "File info:" in output
    assert "File: test.py" in output


def test_full_outcome_without_caller_info():
    """The File info line must not be shown when caller_info is None."""
    data = SimpleExceptionData(problem="Some problem")
    data._get_location = False

    output = SIMPLE(data, validate=False)

    assert "File info:" not in output


# -----------------------------------------------------------------------------
# intercepted_exception
# -----------------------------------------------------------------------------

def test_intercepted_exception_shown_as_last_line():
    """The intercepted exception must be shown as the last part of the output."""
    data = SimpleExceptionData(problem="Some problem")
    data._get_location = False
    data._intercepted_exception = "Expecting value: line 1 column 1"
    data.exception = ValueError

    output = SIMPLE(data, validate=False)

    assert "Intercepted exception (ValueError):" in output
    assert output.endswith("    Expecting value: line 1 column 1")


def test_intercepted_exception_not_shown_when_unset():
    """The intercepted exception must not appear when it is not set."""
    data = SimpleExceptionData(problem="Some problem")
    data._get_location = False

    output = SIMPLE(data, validate=False)

    assert "Intercepted exception" not in output


# -----------------------------------------------------------------------------
# Relationship to PRETTY
# -----------------------------------------------------------------------------

def test_simple_vs_pretty_same_content():
    """SIMPLE and PRETTY must produce identical content — differing only in decorative lines."""
    data = SimpleExceptionData(
        error_name="COMPARE",
        problem="Some problem",
        how_to_fix=("Fix it",)
    )
    data._get_location = False

    out_simple = SIMPLE(data, validate=False)
    out_pretty = PRETTY(data, validate=False)

    cleaned_pretty = "\n".join(
        line for line in out_pretty.split("\n")
        if line != PRETTY.double_line and line != PRETTY.single_line
    ).strip()

    assert out_simple.strip() == cleaned_pretty