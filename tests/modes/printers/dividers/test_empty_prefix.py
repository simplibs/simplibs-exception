from simplibs.exception.modes.printers.dividers.EMPTY_PREFIX import EMPTY_PREFIX


def test_empty_prefix_value():
    assert EMPTY_PREFIX == "\n           "


def test_empty_prefix_is_a_string():
    assert isinstance(EMPTY_PREFIX, str)
