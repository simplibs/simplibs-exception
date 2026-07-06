from simplibs.exception.modes.printers.exception_info.print_expected import (
    print_expected,
)


def test_none_returns_none():
    assert print_expected(None) is None


def test_empty_string_returns_none():
    assert print_expected("") is None


def test_standard_mode_uses_default_prefix():
    assert print_expected("a string") == "Expected:  a string"


def test_standard_mode_uses_custom_prefix():
    assert print_expected("a string", prefix="EXP: ") == "EXP: a string"


def test_log_mode_format():
    assert print_expected("a string", _log_mode=True) == "expected='a string'"


def test_log_mode_ignores_custom_prefix():
    result = print_expected("a string", prefix="EXP: ", _log_mode=True)
    assert result == "expected='a string'"
