import pytest

from simplibs.sentinels import UNSET
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings
from simplibs.exception.modes.printers.exception_info.print_value_with_type import (
    print_value_with_type,
)


def test_unset_value_returns_none():
    """Confirms that when the value is the internal UNSET sentinel, the printer gracefully yields None to skip the row."""
    assert print_value_with_type(UNSET) is None


def test_standard_mode_includes_repr_and_type():
    """Validates the standard output format, ensuring integers display their raw literal and core python type wrapper."""
    result = print_value_with_type(42)
    assert result == "Got:       42 (int)"


def test_standard_mode_string_value_uses_repr_quotes():
    """Ensures that string payloads retain their native representation quotes within the human-readable display matrix."""
    result = print_value_with_type("hello")
    assert result == "Got:       'hello' (str)"


def test_standard_mode_custom_prefix():
    """Verifies layout flexibility by ensuring the value printer accepts and accurately applies a customized prefix layout."""
    result = print_value_with_type(42, prefix="Value: ")
    assert result == "Value: 42 (int)"


def test_truncation_applied_when_repr_exceeds_max_length():
    """
    Verifies the Truncation Engine: lengths exceeding the threshold must be sliced, 
    appending an exact calculation notice of the hidden characters.
    """
    long_value = "x" * 100
    result = print_value_with_type(long_value, max_length=10)

    assert "truncated" in result
    # repr('x'*100) adds 2 outer quote characters = 102 total length. 102 - 10 (max) = 92 truncated.
    assert "92 chars" in result


def test_no_truncation_when_under_max_length():
    """Ensures that if the representation length remains below the strict threshold, no truncation indicators are injected."""
    result = print_value_with_type("short", max_length=100)
    assert "truncated" not in result


def test_falls_back_to_global_settings_truncation_length():
    """Validates fallback routing: if a local max_length override is omitted, the engine successfully queries global settings."""
    SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH = 5
    result = print_value_with_type("a much longer string value")
    assert "truncated" in result


def test_log_mode_untruncated_value():
    """Verifies that in Log Mode, a standard primitive value formats cleanly as plain key-value attributes."""
    result = print_value_with_type(42, _log_mode=True)
    assert result == "value=42 type=int"


def test_log_mode_string_value():
    """Verifies that in Log Mode, string values emit their natural repr quotes seamlessly without duplicate encapsulation."""
    result = print_value_with_type("hello", _log_mode=True)
    assert result == "value='hello' type=str"


def test_log_mode_truncated_value_is_rewrapped_with_repr():
    """
    Architectural Contract: Verifies Log Row Safety. If a payload is truncated, the resulting string 
    contains free-form spaces. The engine must re-wrap the final string using repr (!r) to ensure 
    space-delimited log aggregators capture it as a single bounded field.
    """
    long_value = "x" * 50
    result = print_value_with_type(long_value, max_length=10, _log_mode=True)

    assert result.startswith("value=")
    assert "type=str" in result
    assert "truncated" in result

    # 50 chars of 'x' + 2 quotes = 52 total repr length.
    # Slicing at max_length=10 takes: 1 quote + 9 chars of 'x'.
    # Then re-wrapping with repr turns the outer boundary into double quotes (").
    assert 'value="\'xxxxxxxxx... [truncated, 42 chars]"' in result


