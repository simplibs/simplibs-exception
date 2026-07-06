from simplibs.exception.modes.printers.exception_info.print_value_with_type import (
    print_value_with_type,
)
from simplibs.exception.SimpleExceptionData import SimpleExceptionData
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings

# Obtain the real UNSET sentinel indirectly (its exact module path isn't
# something we want to hard-code/guess), via the field default of
# SimpleExceptionData.value.
UNSET = SimpleExceptionData().value


def test_unset_value_returns_none():
    assert print_value_with_type(UNSET) is None


def test_standard_mode_includes_repr_and_type():
    result = print_value_with_type(42)
    assert result == "Got:       42 (int)"


def test_standard_mode_string_value_uses_repr_quotes():
    result = print_value_with_type("hello")
    assert result == "Got:       'hello' (str)"


def test_standard_mode_custom_prefix():
    result = print_value_with_type(42, prefix="Value: ")
    assert result == "Value: 42 (int)"


def test_truncation_applied_when_repr_exceeds_max_length():
    long_value = "x" * 100
    result = print_value_with_type(long_value, max_length=10)
    assert "truncated" in result
    # repr('x'*100) is 102 chars (2 quote chars added); 102 - max_length(10) = 92
    assert "92 chars" in result


def test_no_truncation_when_under_max_length():
    result = print_value_with_type("short", max_length=100)
    assert "truncated" not in result


def test_falls_back_to_global_settings_truncation_length():
    SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH = 5
    result = print_value_with_type("a much longer string value")
    assert "truncated" in result


def test_log_mode_untruncated_value():
    result = print_value_with_type(42, _log_mode=True)
    assert result == "value=42 type=int"


def test_log_mode_string_value():
    result = print_value_with_type("hello", _log_mode=True)
    assert result == "value='hello' type=str"


def test_log_mode_truncated_value_is_rewrapped_with_repr():
    long_value = "x" * 50
    result = print_value_with_type(long_value, max_length=10, _log_mode=True)
    assert result.startswith("value=")
    assert "type=str" in result
    assert "truncated" in result
