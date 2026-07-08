from simplibs.exception.modes.printers.dividers.DOT_PREFIX import DOT_PREFIX


def test_dot_prefix_value():
    """Confirms the absolute character layout block of the dot prefix to guarantee visual alignment symmetry."""
    assert DOT_PREFIX == "\n     • "


def test_dot_prefix_is_a_string():
    """Validates that the prefix asset is bound strictly to a string primitive type for seamless layout concatenation."""
    assert isinstance(DOT_PREFIX, str)


def test_dot_prefix_anatomical_structure():
    """
    Architectural Contract: Verifies the structural composition of the layout asset.
    It must start with a newline to break the layout, follow up with exact spacing, and end with a bullet token.
    """
    assert DOT_PREFIX.startswith("\n")
    assert DOT_PREFIX.endswith("• ")

    # Verify that the internal padding contains exactly 5 spaces between newline and bullet
    padding = DOT_PREFIX[1:-2]
    assert padding == "     "
    assert len(padding) == 5