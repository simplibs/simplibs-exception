from simplibs.exception.modes.printers.exception_info_multiline.print_context import (
    print_context,
)
from simplibs.exception.modes.printers.dividers.EMPTY_PREFIX import EMPTY_PREFIX


def test_none_returns_none():
    assert print_context(None) is None


def test_empty_tuple_returns_none():
    assert print_context(()) is None


def test_string_fast_path_standard_mode():
    assert print_context("single line") == "Context:   single line"


def test_string_fast_path_log_mode():
    assert print_context("single line", _log_mode=True) == "context='single line'"


def test_single_item_tuple_standard_mode():
    assert print_context(("only one",)) == "Context:   only one"


def test_multi_item_tuple_standard_mode_uses_empty_prefix_alignment():
    result = print_context(("first", "second", "third"))
    expected = "Context:   first" + EMPTY_PREFIX + EMPTY_PREFIX.join(("second", "third"))
    assert result == expected


def test_multi_item_tuple_oneline_mode_inlines_with_spaces():
    result = print_context(("first", "second", "third"), _oneline=True)
    assert result == "Context:   first second third"


def test_multi_item_tuple_log_mode_flattens():
    result = print_context(("first", "second"), _log_mode=True)
    assert result == "context='first second'"


def test_custom_prefix_is_respected():
    result = print_context(("only one",), prefix="CTX: ")
    assert result == "CTX: only one"
