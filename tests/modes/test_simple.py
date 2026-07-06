from simplibs.exception.modes.SIMPLE import SIMPLE
from simplibs.exception.modes.printers.dividers.DOUBLE_LINE import DOUBLE_LINE
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


def test_render_never_includes_decorative_double_lines():
    result = SIMPLE.render(_FullData(), validate=False)
    assert DOUBLE_LINE not in result


def test_render_includes_header_with_label():
    result = SIMPLE.render(_FullData(), validate=False)
    assert result.startswith("⚠️ ERROR: my-label")


def test_render_includes_all_populated_fields():
    result = SIMPLE.render(_FullData(), validate=False)
    assert "Message:   my message" in result
    assert "Expected:  expected thing" in result
    assert "Got:       42 (int)" in result
    assert "Problem:   the problem" in result
    assert "Context:   the context" in result
    assert "🔧 How to fix:" in result


def test_render_handles_empty_data_gracefully():
    result = SIMPLE.render(_EmptyData(), validate=False)
    assert result == "⚠️ ERROR"


def test_singleton_repr():
    assert repr(SIMPLE) == "<SimpleMessage mode>"
