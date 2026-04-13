"""
Tests for PRETTY mode — double line framing, field content, field order, and intercepted exception.
"""
import pytest
from unittest.mock import MagicMock
from simplibs.exception.modes.PRETTY import PRETTY
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData
from simplibs.sentinels import UNSET

@pytest.fixture
def pretty_data():
    """Provides a Mock of SimpleExceptionData configured for PRETTY mode tests."""
    data = MagicMock(spec=SimpleExceptionData)
    data.error_name = "PRETTY_TEST"
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

def test_no_none_in_output(pretty_data):
    """The output must not contain the string 'None' anywhere — UNSET fields are skipped."""
    pretty_data.problem = "Only problem"
    pretty_data._get_location = False

    output = PRETTY(pretty_data, validate=False)

    assert "None" not in output


# -----------------------------------------------------------------------------
# _empty_outcome
# -----------------------------------------------------------------------------

def test_empty_outcome_is_wrapped_in_double_lines(pretty_data):
    """The empty output must be framed with double lines."""
    pretty_data.error_name = "EMPTY_TEST"
    pretty_data._get_location = False

    output = PRETTY(pretty_data, validate=False)
    lines = output.strip().split("\n")

    assert lines[0] == PRETTY.double_line
    # Intro line now doesn't have a colon if label is missing
    assert "⚠️ EMPTY_TEST" in lines[1]
    assert lines[-1] == PRETTY.double_line


def test_empty_outcome_with_caller_info(pretty_data):
    """Caller info must be included in the empty output when available."""
    pretty_data.error_name = "EMPTY_TEST"

    output = PRETTY(pretty_data, validate=False)

    assert "File: test.py" in output
    assert "Line: 1" in output


# -----------------------------------------------------------------------------
# _message_outcome
# -----------------------------------------------------------------------------

def test_message_outcome_contains_message_and_double_lines(pretty_data):
    """The message output must contain the message (with colon) and be framed with double lines."""
    pretty_data.error_name = "MSG_TEST"
    pretty_data.message = "Something is wrong"
    pretty_data._get_location = False

    output = PRETTY(pretty_data, validate=False)

    # Note the manually added colon in _message_outcome
    assert "⚠️ MSG_TEST: Something is wrong" in output
    assert output.count(PRETTY.double_line) == 2


def test_message_outcome_with_caller_info(pretty_data):
    """Caller info must be included in the message output when available."""
    pretty_data.error_name = "MSG_TEST"
    pretty_data.message = "Something is wrong"

    output = PRETTY(pretty_data, validate=False)

    assert "File: test.py" in output
    assert output.count(PRETTY.double_line) == 2


# -----------------------------------------------------------------------------
# _full_outcome
# -----------------------------------------------------------------------------

def test_full_outcome_contains_all_fields(pretty_data):
    """The full output must contain all provided fields."""
    pretty_data.error_name = "FULL_TEST"
    pretty_data.message = "Failure"
    pretty_data.expected = "int"
    pretty_data.value = 42
    pretty_data.problem = "Mismatched types"
    pretty_data.context = "inside a loop"
    pretty_data.how_to_fix = ("Check types", "Restart")
    pretty_data._get_location = False

    output = PRETTY(pretty_data, validate=False)

    assert "Message:   Failure" in output
    assert "Expected:  int" in output
    assert "Got:       42 (int)" in output
    assert "Problem:   Mismatched types" in output
    assert "Context:   inside a loop" in output
    assert "🔧 How to fix:" in output
    assert "• Check types" in output
    assert "• Restart" in output


def test_full_outcome_field_order(pretty_data):
    """Fields must appear in order: Message, Expected, Got, Problem, Context."""
    pretty_data.message = "a message"
    pretty_data.expected = "str"
    pretty_data.value = 42
    pretty_data.problem = "wrong type"
    pretty_data.context = "context"
    pretty_data._get_location = False

    output = PRETTY(pretty_data, validate=False)

    assert output.index("Message:") < output.index("Expected:")
    assert output.index("Expected:") < output.index("Got:")
    assert output.index("Got:") < output.index("Problem:")
    assert output.index("Problem:") < output.index("Context:")


def test_full_outcome_location_split_into_two_lines(pretty_data):
    """The location info must be split into 'File info' and 'File path' lines."""
    pretty_data.problem = "Some problem"

    output = PRETTY(pretty_data, validate=False)

    assert "File info: File: test.py | Line: 1 | Function: func" in output
    assert "File path: path/test.py" in output
    assert output.index("File info:") < output.index("File path:")


def test_full_outcome_how_to_fix_has_single_line_before_it(pretty_data):
    """A single_line separator must appear before the How to fix section."""
    pretty_data.problem = "an error"
    pretty_data.how_to_fix = ("Fix it",)
    pretty_data._get_location = False

    output = PRETTY(pretty_data, validate=False)

    assert PRETTY.single_line in output
    assert output.index(PRETTY.single_line) < output.index("🔧 How to fix:")


def test_full_outcome_ends_with_double_line_when_no_intercepted(pretty_data):
    """Without an intercepted_exception, the output must end with a double_line."""
    pretty_data.problem = "an error"
    pretty_data._get_location = False

    output = PRETTY(pretty_data, validate=False)

    assert output.strip().endswith(PRETTY.double_line)


def test_full_outcome_without_caller_info_hides_file_info(pretty_data):
    """The File info and path lines must not be shown when caller_info is UNSET or location disabled."""
    pretty_data.problem = "Some problem"
    pretty_data._get_location = False

    output = PRETTY(pretty_data, validate=False)

    assert "File info:" not in output
    assert "File path:" not in output


# -----------------------------------------------------------------------------
# intercepted_exception
# -----------------------------------------------------------------------------

def test_intercepted_exception_shown_below_double_line(pretty_data):
    """The intercepted exception must be shown below the closing double_line."""
    pretty_data.problem = "Some problem"
    pretty_data._get_location = False
    pretty_data._intercepted_exception = "Expecting value: line 1 column 1"
    pretty_data.exception = ValueError

    output = PRETTY(pretty_data, validate=False)

    assert "Intercepted exception (ValueError):" in output
    assert "Expecting value: line 1 column 1" in output
    last_double_line_pos = output.rindex(PRETTY.double_line)
    assert output.index("Intercepted exception") > last_double_line_pos


def test_intercepted_exception_not_shown_when_unset(pretty_data):
    """The intercepted exception must not appear when it is not set."""
    pretty_data.problem = "Some problem"
    pretty_data._get_location = False
    pretty_data._intercepted_exception = UNSET

    output = PRETTY(pretty_data, validate=False)

    assert "Intercepted exception" not in output
    assert output.strip().endswith(PRETTY.double_line)