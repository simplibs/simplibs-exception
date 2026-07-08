from simplibs.exception.modes.printers.dividers.EMPTY_PREFIX import EMPTY_PREFIX


def test_empty_prefix_value():
    """Confirms the absolute character layout block of the empty prefix to guarantee vertical block alignment."""
    assert EMPTY_PREFIX == "\n           "


def test_empty_prefix_is_a_string():
    """Validates that the prefix asset is bound strictly to a string primitive type for seamless layout concatenation."""
    assert isinstance(EMPTY_PREFIX, str)


def test_empty_prefix_has_exact_padding_width():
    """
    Architectural Contract: Enforces absolute mathematical layout alignment. The padding block
    must consist of exactly 11 space characters following the newline to match the standard label matrix.
    """
    assert EMPTY_PREFIX.startswith("\n")

    # Extract the padding component and verify its exact structural characteristics
    padding = EMPTY_PREFIX[1:]
    assert padding == "           "
    assert len(padding) == 11

    # Ensure there is no other pollution (like tabs or unexpected control characters)
    assert all(char == " " for char in padding)