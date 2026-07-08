from simplibs.exception.modes.printers.intro.print_intro import print_intro


def test_standard_mode_with_label():
    """Validates the standard human-readable header composition using the default emoji prefix and identity pairing."""
    result = print_intro("VALIDATION ERROR", "my-label")
    assert result == "⚠️ VALIDATION ERROR: my-label"


def test_standard_mode_without_label():
    """Ensures that omitting the label produces a clean identity header without trailing colons or excess padding."""
    result = print_intro("VALIDATION ERROR", None)
    assert result == "⚠️ VALIDATION ERROR"


def test_standard_mode_custom_prefix():
    """Verifies layout flexibility by ensuring the intro printer accurately applies a customized prefix token."""
    result = print_intro("VALIDATION ERROR", "my-label", prefix=">> ")
    assert result == ">> VALIDATION ERROR: my-label"


def test_log_mode_with_label():
    """Verifies Log Mode behavior: both identity tokens must be cleanly wrapped via repr (!r) for multi-word safety."""
    result = print_intro("VALIDATION ERROR", "my-label", _log_mode=True)
    assert result == "error='VALIDATION ERROR' label='my-label'"


def test_log_mode_without_label():
    """
    Architectural Contract: Verifies Log Mode row compilation when label is omitted.
    Ensures that the core error name identifier is strictly wrapped via repr (!r)
    to prevent space-delimited log parser fragmentation.
    """
    result = print_intro("VALIDATION ERROR", None, _log_mode=True)
    assert result == "error='VALIDATION ERROR'"


def test_empty_string_label_is_treated_as_falsy():
    """Guarantees that empty string labels are treated as falsy/omitted, preventing blank indicators from polluting the render."""
    result = print_intro("VALIDATION ERROR", "")
    assert result == "⚠️ VALIDATION ERROR"


