from simplibs.exception.modes.printers.dividers.DOUBLE_LINE import DOUBLE_LINE


def test_double_line_value():
    """Confirms that the double line divider consists entirely of the correct architectural box-drawing character."""
    assert DOUBLE_LINE == "═" * 65


def test_double_line_length():
    """Validates the precise horizontal length allocation to guarantee strict layout symmetry across all log outputs."""
    assert len(DOUBLE_LINE) == 65


def test_double_line_is_perfectly_homogenous():
    """
    Architectural Contract: Enforces absolute structural purity. The divider must
    contain exclusively the double-line box-drawing character with zero whitespace pollution.
    """
    # Create a set of unique characters present in the string
    unique_chars = set(DOUBLE_LINE)

    # It must contain exactly one type of character, and that character must be '═'
    assert len(unique_chars) == 1
    assert "═" in unique_chars