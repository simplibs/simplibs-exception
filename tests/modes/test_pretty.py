"""
Tests for PRETTY mode — double line framing, field content, field order, and intercepted exception.
"""
import pytest
from unittest.mock import patch
from simplibs.exception.modes.PRETTY import PRETTY
from simplibs.exception.core.data.SimpleExceptionData import SimpleExceptionData


MOCK_CALLER_INFO = {
    "file": "test.py",
    "line": 1,
    "full_path": "path/test.py",
    "function": "func"
}


# -----------------------------------------------------------------------------
# Critical properties
# -----------------------------------------------------------------------------

def test_no_none_in_output():
    """The output must not contain the string 'None' anywhere — UNSET fields are skipped."""
    data = SimpleExceptionData(problem="Only problem")
    data._get_location = False

    output = PRETTY(data, validate=False)

    assert "None" not in output


# -----------------------------------------------------------------------------
# _empty_outcome
# -----------------------------------------------------------------------------

def test_empty_outcome_is_wrapped_in_double_lines():
    """The empty output must be framed with double lines."""
    data = SimpleExceptionData(error_name="EMPTY_TEST")
    data._get_location = False

    output = PRETTY(data, validate=False)
    lines = output.strip().split("\n")

    assert lines[0] == PRETTY.double_line
    assert "⚠️ EMPTY_TEST:" in lines[1]
    assert lines[-1] == PRETTY.double_line


def test_empty_outcome_with_caller_info():
    """Caller info must be included in the empty output when available."""
    data = SimpleExceptionData(error_name="EMPTY_TEST")

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=MOCK_CALLER_INFO):
        output = PRETTY(data, validate=False)

    assert "File: test.py" in output
    assert "Line: 1" in output


# -----------------------------------------------------------------------------
# _message_outcome
# -----------------------------------------------------------------------------

def test_message_outcome_contains_message_and_double_lines():
    """The message output must contain the message and be framed with double lines."""
    data = SimpleExceptionData(error_name="MSG_TEST", message="Something is wrong")
    data._get_location = False

    output = PRETTY(data, validate=False)

    assert "⚠️ MSG_TEST: Something is wrong" in output
    assert output.count(PRETTY.double_line) == 2


def test_message_outcome_with_caller_info():
    """Caller info must be included in the message output when available."""
    data = SimpleExceptionData(error_name="MSG_TEST", message="Something is wrong")

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=MOCK_CALLER_INFO):
        output = PRETTY(data, validate=False)

    assert "File: test.py" in output
    assert output.count(PRETTY.double_line) == 2


# -----------------------------------------------------------------------------
# _full_outcome
# -----------------------------------------------------------------------------

def test_full_outcome_contains_all_fields():
    """The full output must contain all provided fields."""
    data = SimpleExceptionData(
        error_name="FULL_TEST",
        message="Failure",
        expected="int",
        value=42,
        problem="Mismatched types",
        context="inside a loop",
        how_to_fix=("Check types", "Restart"),
    )
    data._get_location = False

    output = PRETTY(data, validate=False)

    assert "Message:   Failure" in output
    assert "Expected:  int" in output
    assert "Got:       42 (int)" in output
    assert "Problem:   Mismatched types" in output
    assert "Context:   inside a loop" in output
    assert "🔧 How to fix:" in output
    assert "• Check types" in output
    assert "• Restart" in output


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

    output = PRETTY(data, validate=False)

    assert output.index("Message:") < output.index("Expected:")
    assert output.index("Expected:") < output.index("Got:")
    assert output.index("Got:") < output.index("Problem:")
    assert output.index("Problem:") < output.index("Context:")


def test_full_outcome_how_to_fix_has_single_line_before_it():
    """A single_line separator must appear before the How to fix section."""
    data = SimpleExceptionData(problem="an error", how_to_fix=("Fix it",))
    data._get_location = False

    output = PRETTY(data, validate=False)

    assert PRETTY.single_line in output
    assert output.index(PRETTY.single_line) < output.index("🔧 How to fix:")


def test_full_outcome_ends_with_double_line_when_no_intercepted():
    """Without an intercepted_exception, the output must end with a double_line."""
    data = SimpleExceptionData(problem="an error")
    data._get_location = False

    output = PRETTY(data, validate=False)

    assert output.endswith(PRETTY.double_line)


def test_full_outcome_with_caller_info_shows_file_info():
    """The File info line must be shown when caller_info is available."""
    data = SimpleExceptionData(problem="Some problem")

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=MOCK_CALLER_INFO):
        output = PRETTY(data, validate=False)

    assert "File info:" in output
    assert "File: test.py" in output


def test_full_outcome_without_caller_info_hides_file_info():
    """The File info line must not be shown when caller_info is None."""
    data = SimpleExceptionData(problem="Some problem")
    data._get_location = False

    output = PRETTY(data, validate=False)

    assert "File info:" not in output


# -----------------------------------------------------------------------------
# intercepted_exception
# -----------------------------------------------------------------------------

def test_intercepted_exception_shown_below_double_line():
    """The intercepted exception must be shown below the closing double_line."""
    data = SimpleExceptionData(problem="Some problem")
    data._get_location = False
    data._intercepted_exception = "Expecting value: line 1 column 1"
    data.exception = ValueError

    output = PRETTY(data, validate=False)

    assert "Intercepted exception (ValueError):" in output
    assert "Expecting value: line 1 column 1" in output
    last_double_line_pos = output.rindex(PRETTY.double_line)
    assert output.index("Intercepted exception") > last_double_line_pos


def test_intercepted_exception_not_shown_when_unset():
    """The intercepted exception must not appear when it is not set."""
    data = SimpleExceptionData(problem="Some problem")
    data._get_location = False

    output = PRETTY(data, validate=False)

    assert "Intercepted exception" not in output
    assert output.endswith(PRETTY.double_line)