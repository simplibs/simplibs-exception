from simplibs.exception.modes.printers.dividers.DOT_PREFIX import DOT_PREFIX
from simplibs.exception.modes.printers.hepl_info_multiline.print_how_to_fix import (
    print_how_to_fix,
)


def test_none_returns_none():
    """Confirms that passing a None mitigation block gracefully yields None, indicating the field should be skipped."""
    assert print_how_to_fix(None) is None


def test_empty_tuple_returns_none():
    """Ensures that empty sequence structures are treated as omitted metadata, preventing empty lines from polluting the render."""
    assert print_how_to_fix(()) is None


def test_string_fast_path_standard_mode():
    """Validates the Primitive String Fast-Path under standard mode, ensuring the single instruction gets pre-injected with a structural bullet."""
    result = print_how_to_fix("do this")
    assert result == "🔧 How to fix:" + DOT_PREFIX + "do this"


def test_string_fast_path_oneline_mode():
    """Validates the Primitive String Fast-Path under Oneline Mode, shifting the layout into a flat space-separated string."""
    result = print_how_to_fix("do this", _oneline=True)
    assert result == "🔧 How to fix: do this"


def test_string_fast_path_log_mode():
    """Validates the Primitive String Fast-Path under Log Mode, ensuring fast repr encapsulation directly from raw string."""
    result = print_how_to_fix("do this", _log_mode=True)
    assert result == "how_to_fix='do this'"


def test_tuple_standard_mode_uses_bulleted_dot_prefix():
    """
    Verifies the Multi-Line Collection Path via the Bullet-Column Pattern:
    every mitigation item, including the first row, must be preceded by an identical vertical bullet layout.
    """
    result = print_how_to_fix(("step one", "step two"))
    expected = "🔧 How to fix:" + DOT_PREFIX + DOT_PREFIX.join(("step one", "step two"))
    assert result == expected


def test_tuple_oneline_mode_inlines_with_spaces():
    """Validates Oneline Mode routing for collections: multi-line steps must collapse into a flat space-separated layout row."""
    result = print_how_to_fix(("step one", "step two"), _oneline=True)
    assert result == "🔧 How to fix: step one step two"


def test_tuple_log_mode_flattens():
    """
    Verifies Log Mode row safety: multi-line mitigation collections must flatten into a single
    space-delimited string token encapsulated securely inside repr quotes.
    """
    result = print_how_to_fix(("step one", "step two"), _log_mode=True)
    assert result == "how_to_fix='step one step two'"


def test_custom_prefix_is_respected():
    """Verifies layout flexibility by ensuring the mitigation printer dynamically applies a customized prefix marker."""
    result = print_how_to_fix("do this", prefix="FIX:")
    assert result == "FIX:" + DOT_PREFIX + "do this"


from simplibs.exception.modes.printers.dividers.DOT_PREFIX import DOT_PREFIX
from simplibs.exception.modes.printers.hepl_info_multiline.print_how_to_fix import (
    print_how_to_fix,
)


def test_none_returns_none():
    """Confirms that passing a None mitigation block gracefully yields None, indicating the field should be skipped."""
    assert print_how_to_fix(None) is None


def test_empty_tuple_returns_none():
    """Ensures that empty sequence structures are treated as omitted metadata, preventing empty lines from polluting the render."""
    assert print_how_to_fix(()) is None


def test_string_fast_path_standard_mode():
    """Validates the Primitive String Fast-Path under standard mode, ensuring the single instruction gets pre-injected with a structural bullet."""
    result = print_how_to_fix("do this")
    assert result == "🔧 How to fix:" + DOT_PREFIX + "do this"


def test_string_fast_path_oneline_mode():
    """Validates the Primitive String Fast-Path under Oneline Mode, shifting the layout into a flat space-separated string."""
    result = print_how_to_fix("do this", _oneline=True)
    assert result == "🔧 How to fix: do this"


def test_string_fast_path_log_mode():
    """Validates the Primitive String Fast-Path under Log Mode, ensuring fast repr encapsulation directly from raw string."""
    result = print_how_to_fix("do this", _log_mode=True)
    assert result == "how_to_fix='do this'"


def test_tuple_standard_mode_uses_bulleted_dot_prefix():
    """
    Verifies the Multi-Line Collection Path via the Bullet-Column Pattern:
    every mitigation item, including the first row, must be preceded by an identical vertical bullet layout.
    """
    result = print_how_to_fix(("step one", "step two"))
    expected = "🔧 How to fix:" + DOT_PREFIX + DOT_PREFIX.join(("step one", "step two"))
    assert result == expected


def test_tuple_oneline_mode_inlines_with_spaces():
    """Validates Oneline Mode routing for collections: multi-line steps must collapse into a flat space-separated layout row."""
    result = print_how_to_fix(("step one", "step two"), _oneline=True)
    assert result == "🔧 How to fix: step one step two"


def test_tuple_log_mode_flattens():
    """
    Verifies Log Mode row safety: multi-line mitigation collections must flatten into a single
    space-delimited string token encapsulated securely inside repr quotes.
    """
    result = print_how_to_fix(("step one", "step two"), _log_mode=True)
    assert result == "how_to_fix='step one step two'"


def test_custom_prefix_is_respected():
    """Verifies layout flexibility by ensuring the mitigation printer dynamically applies a customized prefix marker."""
    result = print_how_to_fix("do this", prefix="FIX:")
    assert result == "FIX:" + DOT_PREFIX + "do this"