"""
Tests for PrintValueWithTypeMixin — value formatting with type, intro prefix, and UNSET handling.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData
from simplibs.exception.modes.mode_base._mixins.PrintValueWithType import PrintValueWithTypeMixin


class MockMode(PrintValueWithTypeMixin):
    pass


@pytest.fixture
def mode():
    return MockMode()


# -----------------------------------------------------------------------------
# PrintValueWithTypeMixin
# -----------------------------------------------------------------------------

def test_string_value_with_intro(mode):
    """String value with intro prefix must be formatted correctly."""
    data = SimpleExceptionData(value="hello")
    assert mode._print_value_with_type(data, intro="Got: ") == "Got: 'hello' (str)"


def test_int_value_with_intro(mode):
    """Int value with intro prefix must be formatted correctly."""
    data = SimpleExceptionData(value=123)
    assert mode._print_value_with_type(data, intro="Value: ") == "Value: 123 (int)"


def test_value_without_intro(mode):
    """Without an intro the value must still be formatted correctly."""
    data = SimpleExceptionData(value=42)
    assert mode._print_value_with_type(data) == "42 (int)"


def test_none_value_is_not_unset(mode):
    """None is not UNSET — must return a formatted string, not None."""
    data = SimpleExceptionData(value=None)
    assert mode._print_value_with_type(data) == "None (NoneType)"


def test_false_value_is_not_unset(mode):
    """False is not UNSET — must return a formatted string, not None."""
    data = SimpleExceptionData(value=False)
    assert mode._print_value_with_type(data) == "False (bool)"


def test_unset_value_returns_none(mode):
    """UNSET value must return None — signals that the line should be skipped."""
    data = SimpleExceptionData(value=UNSET)
    assert mode._print_value_with_type(data) is None