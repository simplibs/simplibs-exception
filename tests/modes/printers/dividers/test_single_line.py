from simplibs.exception.modes.printers.dividers.SINGLE_LINE import SINGLE_LINE


def test_single_line_value():
    assert SINGLE_LINE == "─" * 65


def test_single_line_length():
    assert len(SINGLE_LINE) == 65
