from simplibs.exception.modes.PRETTY import PRETTY
from simplibs.exception.modes.printers.dividers.DOUBLE_LINE import DOUBLE_LINE
from simplibs.exception.modes.printers.dividers.SINGLE_LINE import SINGLE_LINE
from simplibs.exception.SimpleExceptionData import SimpleExceptionData

UNSET = SimpleExceptionData().value


class _FullData:
    error_name = "ERROR"
    label = "my-label"
    message = "my message"
    expected = "expected thing"
    value = 42
    problem = "the problem"
    context = "the context"
    how_to_fix = "fix it"
    caller_info = None
    exception = None


class _MessageOnlyData:
    error_name = "ERROR"
    label = None
    message = "just a message"
    expected = None
    value = UNSET
    problem = None
    context = None
    how_to_fix = None
    caller_info = None
    exception = None


class _EmptyData:
    error_name = "ERROR"
    label = None
    message = None
    expected = None
    value = UNSET
    problem = None
    context = None
    how_to_fix = None
    caller_info = None
    exception = None


def test_render_starts_and_wraps_with_double_line():
    result = PRETTY.render(_FullData(), validate=False)
    lines = result.split("\n")
    assert lines[0] == DOUBLE_LINE


def test_render_includes_header_with_label():
    result = PRETTY.render(_FullData(), validate=False)
    assert "⚠️ ERROR: my-label" in result


def test_render_includes_second_double_line_when_details_present():
    result = PRETTY.render(_FullData(), validate=False)
    # start + post-intro (has_details) + closing = 3
    assert result.count(DOUBLE_LINE) == 3


def test_render_omits_second_double_line_when_no_details():
    result = PRETTY.render(_MessageOnlyData(), validate=False)
    # Only the closing DOUBLE_LINE should be present, not a second one right
    # after the header, since expected/value/problem/context are all absent.
    assert result.count(DOUBLE_LINE) == 2  # opening + closing framing lines


def test_render_includes_single_line_before_how_to_fix():
    result = PRETTY.render(_FullData(), validate=False)
    assert SINGLE_LINE in result
    assert "🔧 How to fix:" in result


def test_render_omits_single_line_when_no_how_to_fix():
    result = PRETTY.render(_MessageOnlyData(), validate=False)
    assert SINGLE_LINE not in result


def test_render_handles_fully_empty_data_gracefully():
    result = PRETTY.render(_EmptyData(), validate=False)
    assert "⚠️ ERROR" in result
    assert isinstance(result, str)


def test_render_includes_value_with_type():
    result = PRETTY.render(_FullData(), validate=False)
    assert "Got:       42 (int)" in result


def test_singleton_repr():
    assert repr(PRETTY) == "<PrettyMessage mode>"
