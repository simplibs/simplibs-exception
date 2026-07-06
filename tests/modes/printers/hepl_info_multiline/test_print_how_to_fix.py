from simplibs.exception.modes.printers.hepl_info_multiline.print_how_to_fix import (
    print_how_to_fix,
)
from simplibs.exception.modes.printers.dividers.DOT_PREFIX import DOT_PREFIX


def test_none_returns_none():
    assert print_how_to_fix(None) is None


def test_empty_tuple_returns_none():
    assert print_how_to_fix(()) is None


def test_string_fast_path_standard_mode():
    result = print_how_to_fix("do this")
    assert result == "🔧 How to fix:" + DOT_PREFIX + "do this"


def test_string_fast_path_oneline_mode():
    result = print_how_to_fix("do this", _oneline=True)
    assert result == "🔧 How to fix: do this"


def test_string_fast_path_log_mode():
    result = print_how_to_fix("do this", _log_mode=True)
    assert result == "how_to_fix='do this'"


def test_tuple_standard_mode_uses_bulleted_dot_prefix():
    result = print_how_to_fix(("step one", "step two"))
    expected = "🔧 How to fix:" + DOT_PREFIX + DOT_PREFIX.join(("step one", "step two"))
    assert result == expected


def test_tuple_oneline_mode_inlines_with_spaces():
    result = print_how_to_fix(("step one", "step two"), _oneline=True)
    assert result == "🔧 How to fix: step one step two"


def test_tuple_log_mode_flattens():
    result = print_how_to_fix(("step one", "step two"), _log_mode=True)
    assert result == "how_to_fix='step one step two'"


def test_custom_prefix_is_respected():
    result = print_how_to_fix("do this", prefix="FIX:")
    assert result == "FIX:" + DOT_PREFIX + "do this"
