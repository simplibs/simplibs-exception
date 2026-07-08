from simplibs.exception.modes.printers.dividers.EMPTY_PREFIX import EMPTY_PREFIX
from simplibs.exception.modes.printers.exception_info_multiline.print_problem import (
    print_problem,
)


def test_none_returns_none():
    """Confirms that passing a None problem gracefully yields None, indicating the field should be skipped in the layout."""
    assert print_problem(None) is None


def test_empty_tuple_returns_none():
    """Ensures that empty sequence structures are treated as omitted metadata, preventing empty lines from polluting the render."""
    assert print_problem(()) is None


def test_string_fast_path_standard_mode():
    """Validates the Primitive String Fast-Path under standard mode, bypassing collection slicing for high performance."""
    assert print_problem("single line") == "Problem:   single line"


def test_string_fast_path_log_mode():
    """Validates the Primitive String Fast-Path under Log Mode, ensuring fast repr encapsulation directly from raw string."""
    assert print_problem("single line", _log_mode=True) == "problem='single line'"


def test_single_item_tuple_standard_mode():
    """Ensures that a single-item collection layout is rendered safely without appending trailing delimiters or whitespace."""
    assert print_problem(("only one",)) == "Problem:   only one"


def test_multi_item_tuple_standard_mode_uses_empty_prefix_alignment():
    """
    Verifies the Multi-Line Collection Path via the Inline-First Pattern:
    subsequent sequence lines must form a perfectly vertical column aligned via EMPTY_PREFIX.
    """
    result = print_problem(("first", "second", "third"))
    expected = "Problem:   first" + EMPTY_PREFIX + EMPTY_PREFIX.join(("second", "third"))
    assert result == expected


def test_multi_item_tuple_oneline_mode_inlines_with_spaces():
    """Validates Oneline Mode routing: multi-line collections must collapse into a flat space-separated layout row."""
    result = print_problem(("first", "second", "third"), _oneline=True)
    assert result == "Problem:   first second third"


def test_multi_item_tuple_log_mode_flattens():
    """
    Verifies Log Mode row safety: multi-line collections must flatten into a single
    space-delimited string token encapsulated securely inside repr quotes.
    """
    result = print_problem(("first", "second"), _log_mode=True)
    assert result == "problem='first second'"


def test_custom_prefix_is_respected():
    """Verifies layout flexibility by ensuring the multi-line printer dynamically applies a customized prefix marker."""
    result = print_problem(("only one",), prefix="PRB: ")
    assert result == "PRB: only one"


def test_log_mode_safely_sanitizes_multiline_collections_containing_hazardous_characters():
    """
    Architectural Contract: Verifies that log mode successfully flattens and sanitizes collection
    items containing raw internal quotes, backslashes, or control characters via repr encapsulation,
    preventing row splitting.
    """
    # A multi-line collection containing raw internal quotes and an embedded newline
    hazardous_collection = ("Query 'SELECT' failed", "Timeout\nencountered.")

    result = print_problem(hazardous_collection, _log_mode=True)

    # Assert that items are joined with space and the whole payload is flattened and safely escaped
    assert result == "problem=\"Query 'SELECT' failed Timeout\\nencountered.\""