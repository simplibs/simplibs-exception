from simplibs.exception.modes.printers.dividers.DOT_PREFIX import DOT_PREFIX


def test_dot_prefix_value():
    assert DOT_PREFIX == "\n     • "


def test_dot_prefix_is_a_string():
    assert isinstance(DOT_PREFIX, str)
