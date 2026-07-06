from simplibs.exception.modes.printers.intro.print_intro import print_intro


def test_standard_mode_with_label():
    result = print_intro("VALIDATION ERROR", "my-label")
    assert result == "⚠️ VALIDATION ERROR: my-label"


def test_standard_mode_without_label():
    result = print_intro("VALIDATION ERROR", None)
    assert result == "⚠️ VALIDATION ERROR"


def test_standard_mode_custom_prefix():
    result = print_intro("VALIDATION ERROR", "my-label", prefix=">> ")
    assert result == ">> VALIDATION ERROR: my-label"


def test_log_mode_with_label():
    result = print_intro("VALIDATION ERROR", "my-label", _log_mode=True)
    assert result == "error='VALIDATION ERROR' label='my-label'"


def test_log_mode_without_label():
    result = print_intro("VALIDATION ERROR", None, _log_mode=True)
    assert result == "error=VALIDATION ERROR"


def test_empty_string_label_is_treated_as_falsy():
    result = print_intro("VALIDATION ERROR", "")
    assert result == "⚠️ VALIDATION ERROR"
