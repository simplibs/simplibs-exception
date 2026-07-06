from simplibs.exception.modes.printers.exception_info_multiline.print_problem import (
    print_problem,
)
from simplibs.exception.modes.printers.dividers.EMPTY_PREFIX import EMPTY_PREFIX


def test_none_returns_none():
    assert print_problem(None) is None


def test_empty_tuple_returns_none():
    assert print_problem(()) is None


def test_string_fast_path_standard_mode():
    assert print_problem("single line") == "Problem:   single line"


def test_string_fast_path_log_mode():
    assert print_problem("single line", _log_mode=True) == "problem='single line'"


def test_single_item_tuple_standard_mode():
    assert print_problem(("only one",)) == "Problem:   only one"


def test_multi_item_tuple_standard_mode_uses_empty_prefix_alignment():
    result = print_problem(("first", "second", "third"))
    expected = "Problem:   first" + EMPTY_PREFIX + EMPTY_PREFIX.join(("second", "third"))
    assert result == expected


def test_multi_item_tuple_oneline_mode_inlines_with_spaces():
    result = print_problem(("first", "second", "third"), _oneline=True)
    assert result == "Problem:   first second third"


def test_multi_item_tuple_log_mode_flattens():
    result = print_problem(("first", "second"), _log_mode=True)
    assert result == "problem='first second'"


def test_custom_prefix_is_respected():
    result = print_problem(("only one",), prefix="PRB: ")
    assert result == "PRB: only one"
