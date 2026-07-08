"""
Tests for SIMPLE mode — no decorative lines, field content, field order, and parity with PRETTY.
"""
import pytest
from unittest.mock import MagicMock
from simplibs.exception.modes.SIMPLE import SIMPLE
from simplibs.exception.modes.PRETTY import PRETTY
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData
from simplibs.sentinels import UNSET

@pytest.fixture
def simple_data():
    """Provides a Mock of SimpleExceptionData configured for SIMPLE mode tests."""
    data = MagicMock(spec=SimpleExceptionData)
    data.error_name = "SIMPLE_TEST"
    data.message = UNSET
    data.value_label = UNSET
    data.value = UNSET
    data.expected = UNSET
    data.problem = UNSET
    data.context = UNSET
    data.how_to_fix = UNSET
    data._get_location = True
    data._intercepted_exception = UNSET
    data.exception = None
    data.caller_info = {
        "file": "test.py",
        "line": 1,
        "full_path": "path/test.py",
        "function": "func"
    }
    return data


# -----------------------------------------------------------------------------
# Critical properties
# -----------------------------------------------------------------------------

def test_no_decorative_lines_in_any_output(simple_data):
    """SIMPLE must never contain decorative lines ═ or ─."""
    simple_data.error_name = "FULL_SIMPLE"
    simple_data.problem = "Network timeout"
    simple_data.how_to_fix = ("Check connection",)
    simple_data._get_location = False

    output = SIMPLE(simple_data, validate=False)

    assert "═" not in output
    assert "─" not in output


def test_no_none_in_output(simple_data):
    """The output must not contain the string 'None' anywhere — UNSET fields are skipped."""
    simple_data.problem = "Only problem"
    simple_data._get_location = False

    output = SIMPLE(simple_data, validate=False)

    assert "None" not in output


# -----------------------------------------------------------------------------
# _empty_outcome (inherited from ModeBase)
# -----------------------------------------------------------------------------

def test_empty_outcome_starts_with_error_name(simple_data):
    """The empty output must start with the error name without any decoration."""
    simple_data.error_name = "SIMPLE_TEST"
    simple_data._get_location = False

    output = SIMPLE(simple_data, validate=False)

    assert output.startswith("⚠️ SIMPLE_TEST")


def test_empty_outcome_with_caller_info(simple_data):
    """Caller info must be included in the empty output when available."""
    simple_data.error_name = "SIMPLE_TEST"

    output = SIMPLE(simple_data, validate=False)

    assert "File: test.py" in output
    assert "Line: 1" in output


# -----------------------------------------------------------------------------
# _full_outcome
# -----------------------------------------------------------------------------

def test_full_outcome_contains_all_fields(simple_data):
    """The full output must contain all provided fields."""
    simple_data.error_name = "FULL_SIMPLE"
    simple_data.message = "a message"
    simple_data.expected = "str"
    simple_data.value = 42
    simple_data.problem = "Network timeout"
    simple_data.context = "inside a loop"
    simple_data.how_to_fix = ("Check connection",)
    simple_data._get_location = False

    output = SIMPLE(simple_data, validate=False)

    assert "⚠️ FULL_SIMPLE" in output
    assert "Message:   a message" in output
    assert "Expected:  str" in output
    assert "Got:       42 (int)" in output
    assert "Problem:   Network timeout" in output
    assert "Context:   inside a loop" in output
    assert "How to fix:" in output
    assert "• Check connection" in output


def test_full_outcome_field_order(simple_data):
    """Fields must appear in order: Message, Expected, Got, Problem, Context."""
    simple_data.message = "a message"
    simple_data.expected = "str"
    simple_data.value = 42
    simple_data.problem = "wrong type"
    simple_data.context = "context"
    simple_data._get_location = False

    output = SIMPLE(simple_data, validate=False)

    assert output.index("Message:") < output.index("Expected:")
    assert output.index("Expected:") < output.index("Got:")
    assert output.index("Got:") < output.index("Problem:")
    assert output.index("Problem:") < output.index("Context:")


def test_full_outcome_location_split_into_two_lines(simple_data):
    """The location info must be split into 'File info' and 'File path' lines."""
    simple_data.problem = "Some problem"

    output = SIMPLE(simple_data, validate=False)

    assert "File info: File: test.py | Line: 1 | Function: func" in output
    assert "File path: path/test.py" in output
    assert output.index("File info:") < output.index("File path:")


def test_full_outcome_without_caller_info(simple_data):
    """The File info and path lines must not be shown when location is disabled."""
    simple_data.problem = "Some problem"
    simple_data._get_location = False

    output = SIMPLE(simple_data, validate=False)

    assert "File info:" not in output
    assert "File path:" not in output


# -----------------------------------------------------------------------------
# intercepted_exception
# -----------------------------------------------------------------------------

def test_intercepted_exception_shown_as_last_line(simple_data):
    """The intercepted exception must be shown as the last part of the output."""
    simple_data.problem = "Some problem"
    simple_data._get_location = False
    simple_data._intercepted_exception = "Expecting value: line 1 column 1"
    simple_data.exception = ValueError

    output = SIMPLE(simple_data, validate=False).strip()

    assert "Intercepted exception (ValueError):" in output
    assert output.endswith("    Expecting value: line 1 column 1")


def test_intercepted_exception_not_shown_when_unset(simple_data):
    """The intercepted exception must not appear when it is not set."""
    simple_data.problem = "Some problem"
    simple_data._get_location = False
    simple_data._intercepted_exception = UNSET

    output = SIMPLE(simple_data, validate=False)

    assert "Intercepted exception" not in output


# -----------------------------------------------------------------------------
# Relationship to PRETTY
# -----------------------------------------------------------------------------

def test_simple_vs_pretty_same_content(simple_data):
    """SIMPLE and PRETTY must produce identical content — differing only in decorative lines."""
    simple_data.error_name = "COMPARE"
    simple_data.problem = "Some problem"
    simple_data.how_to_fix = ("Fix it",)
    simple_data._get_location = False

    out_simple = SIMPLE(simple_data, validate=False)
    out_pretty = PRETTY(simple_data, validate=False)

    cleaned_pretty = "\n".join(
        line for line in out_pretty.split("\n")
        if line != PRETTY.double_line and line != PRETTY.single_line
    ).strip()

    assert out_simple.strip() == cleaned_pretty