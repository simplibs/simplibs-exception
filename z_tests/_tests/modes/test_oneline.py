"""
Tests for ONELINE mode — single-line guarantee, field content, field order, and location handling.
"""
import pytest
from unittest.mock import MagicMock
from simplibs.exception.modes.ONELINE import ONELINE
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData
from simplibs.sentinels import UNSET

MOCK_CALLER_INFO_STR = "File: t.py | Line: 1 | Path: path/t.py | Function: func"


@pytest.fixture
def oneline_data():
    """Provides a Mock of SimpleExceptionData configured for ONELINE mode tests."""
    data = MagicMock(spec=SimpleExceptionData)
    data.error_name = "ONELINE_TEST"
    data.message = UNSET
    data.value_label = UNSET
    data.value = UNSET
    data.expected = UNSET
    data.problem = UNSET
    data.context = UNSET
    data.how_to_fix = UNSET
    data._get_location = True
    # formatted string from PrintCallerInfoMixin
    data.caller_info = {
        "file": "t.py",
        "line": 1,
        "full_path": "path/t.py",
        "function": "func"
    }
    return data


# -----------------------------------------------------------------------------
# Critical properties
# -----------------------------------------------------------------------------

def test_oneline_is_single_line(oneline_data):
    """The output must never contain a newline character."""
    oneline_data.message = "This is a long message"
    oneline_data.problem = "Some problem"

    output = ONELINE(oneline_data, validate=False)

    assert "\n" not in output.strip()


def test_no_none_in_output(oneline_data):
    """The output must not contain the string 'None' anywhere — UNSET fields are skipped."""
    oneline_data.problem = "Only problem"
    oneline_data._get_location = False

    output = ONELINE(oneline_data, validate=False)

    assert "None" not in output


def test_no_empty_separators(oneline_data):
    """UNSET fields must not leave empty pipes '||' or trailing pipes in the output."""
    oneline_data.error_name = "FILTER"
    oneline_data.expected = "Valid string"
    oneline_data._get_location = False

    output = ONELINE(oneline_data, validate=False)

    assert "||" not in output
    assert " |  | " not in output
    assert not output.strip().endswith("|")


# -----------------------------------------------------------------------------
# _empty_outcome
# -----------------------------------------------------------------------------

def test_empty_outcome_with_caller_info(oneline_data):
    """An empty call with caller_info must contain the error name and location."""
    oneline_data.error_name = "EMPTY"

    output = ONELINE(oneline_data, validate=False)

    assert output.startswith("⚠️ EMPTY |")
    assert "File: t.py" in output
    assert "Line: 1" in output


def test_empty_outcome_without_caller_info(oneline_data):
    """An empty call with location enabled but missing info must show 'Location: Unknown'."""
    oneline_data.error_name = "EMPTY"
    oneline_data.caller_info = None

    output = ONELINE(oneline_data, validate=False)

    assert output.startswith("⚠️ EMPTY |")
    assert "Location: Unknown" in output


# -----------------------------------------------------------------------------
# _message_outcome
# -----------------------------------------------------------------------------

def test_message_outcome_format(oneline_data):
    """A message-only call must follow 'INTRO message | LOCATION' format."""
    oneline_data.error_name = "MSG"
    oneline_data.message = "something went wrong"
    oneline_data._get_location = False

    output = ONELINE(oneline_data, validate=False)

    # Note: _print_intro_line provides the "⚠️ MSG:" part
    assert output.startswith("⚠️ MSG: something went wrong |")


# -----------------------------------------------------------------------------
# _full_outcome
# -----------------------------------------------------------------------------

def test_full_outcome_contains_all_fields(oneline_data):
    """The full output must contain all provided fields in string representation."""
    oneline_data.error_name = "FULL"
    oneline_data.value_label = "parameter"
    oneline_data.message = "free-form message"
    oneline_data.expected = "str"
    oneline_data.value = 42
    oneline_data.problem = "wrong type"
    oneline_data.context = "inside loop ID=5"
    oneline_data._get_location = False

    output = ONELINE(oneline_data, validate=False)

    assert "⚠️ FULL: parameter" in output
    assert "Message: free-form message" in output
    assert "Expected: str" in output
    assert "Got: 42 (int)" in output  # from _print_value_with_type
    assert "Problem: wrong type" in output
    assert "Context: inside loop ID=5" in output


def test_full_outcome_field_order(oneline_data):
    """Fields must appear in the defined order (Intro -> Msg -> Expected -> Got -> Problem -> Context)."""
    oneline_data.error_name = "ORDER"
    oneline_data.value_label = "parameter"
    oneline_data.message = "a message"
    oneline_data.expected = "str"
    oneline_data.value = 42
    oneline_data.problem = "wrong type"
    oneline_data.context = "context"
    oneline_data._get_location = False

    output = ONELINE(oneline_data, validate=False)

    # Verify positions
    idx_intro = output.index("ORDER: parameter")
    idx_msg = output.index("Message:")
    idx_exp = output.index("Expected:")
    idx_got = output.index("Got:")
    idx_prob = output.index("Problem:")
    idx_ctx = output.index("Context:")

    assert idx_intro < idx_msg < idx_exp < idx_got < idx_prob < idx_ctx


def test_full_outcome_location_segment_skipped_when_disabled(oneline_data):
    """If _get_location is False, the location segment must be missing entirely."""
    oneline_data.problem = "error"
    oneline_data._get_location = False

    output = ONELINE(oneline_data, validate=False)

    assert "File:" not in output
    assert "Line:" not in output
    assert "Location: Unknown" not in output


def test_full_outcome_how_to_fix_is_intentionally_hidden(oneline_data):
    """how_to_fix must not be rendered in ONELINE mode even if present."""
    oneline_data.how_to_fix = ("Step 1", "Step 2")
    oneline_data.problem = "some problem"
    oneline_data._get_location = False

    output = ONELINE(oneline_data, validate=False)

    assert "Step 1" not in output
    assert "Step 2" not in output