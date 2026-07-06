from simplibs.exception.modes.printers.dividers.DOUBLE_LINE import DOUBLE_LINE


def test_double_line_value():
    assert DOUBLE_LINE == "═" * 65


def test_double_line_length():
    assert len(DOUBLE_LINE) == 65
