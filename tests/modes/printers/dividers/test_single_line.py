from simplibs.exception.modes.printers.dividers.SINGLE_LINE import SINGLE_LINE


def test_single_line_value():
    """Confirms that the single line divider consists entirely of the correct light box-drawing character."""
    assert SINGLE_LINE == "─" * 65


def test_single_line_length():
    """Validates the precise horizontal length allocation to guarantee alignment symmetry with the outer framing."""
    assert len(SINGLE_LINE) == 65


def test_single_line_is_perfectly_homogenous():
    """
    Architectural Contract: Enforces absolute structural purity. The divider must
    contain exclusively the light single-line box-drawing character with zero whitespace pollution.
    """
    # Create a set of unique characters present in the string
    unique_chars = set(SINGLE_LINE)

    # It must contain exactly one type of character, and that character must be '─'
    assert len(unique_chars) == 1
    assert "─" in unique_chars