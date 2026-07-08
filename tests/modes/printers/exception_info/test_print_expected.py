from simplibs.exception.modes.printers.exception_info.print_expected import (
    print_expected,
)


def test_none_returns_none():
    """Confirms that passing a None value gracefully yields None, indicating the field should be skipped in the layout."""
    assert print_expected(None) is None


def test_empty_string_returns_none():
    """Ensures that empty string inputs are treated as omitted metadata, preventing blank lines from polluting the render."""
    assert print_expected("") is None


def test_standard_mode_uses_default_prefix():
    """Validates the standard human-friendly layout, enforcing the default 11-character padded prefix matrix alignment."""
    assert print_expected("a string") == "Expected:  a string"


def test_standard_mode_uses_custom_prefix():
    """Verifies layout flexibility by ensuring the printer accepts and accurately applies a customized prefix layout."""
    assert print_expected("a string", prefix="EXP: ") == "EXP: a string"


def test_log_mode_format():
    """
    Verifies Log Mode behavior: the output must be formatted as a single key-value token,
    utilizing strict repr encapsulation (!r) for safe space-delimited text log parsing.
    """
    assert print_expected("a string", _log_mode=True) == "expected='a string'"


def test_log_mode_ignores_custom_prefix():
    """Guarantees that when _log_mode=True is engaged, any passed custom prefix arguments are safely bypassed to enforce log schema uniformity."""
    result = print_expected("a string", prefix="EXP: ", _log_mode=True)
    assert result == "expected='a string'"


from simplibs.exception.modes.printers.exception_info.print_expected import (
    print_expected,
)


def test_none_returns_none():
    """Confirms that passing a None value gracefully yields None, indicating the field should be skipped in the layout."""
    assert print_expected(None) is None


def test_empty_string_returns_none():
    """Ensures that empty string inputs are treated as omitted metadata, preventing blank lines from polluting the render."""
    assert print_expected("") is None


def test_standard_mode_uses_default_prefix():
    """Validates the standard human-friendly layout, enforcing the default 11-character padded prefix matrix alignment."""
    assert print_expected("a string") == "Expected:  a string"


def test_standard_mode_uses_custom_prefix():
    """Verifies layout flexibility by ensuring the printer accepts and accurately applies a customized prefix layout."""
    assert print_expected("a string", prefix="EXP: ") == "EXP: a string"


def test_log_mode_format():
    """
    Verifies Log Mode behavior: the output must be formatted as a single key-value token,
    utilizing strict repr encapsulation (!r) for safe space-delimited text log parsing.
    """
    assert print_expected("a string", _log_mode=True) == "expected='a string'"


def test_log_mode_ignores_custom_prefix():
    """Guarantees that when _log_mode=True is engaged, any passed custom prefix arguments are safely bypassed to enforce log schema uniformity."""
    result = print_expected("a string", prefix="EXP: ", _log_mode=True)
    assert result == "expected='a string'"