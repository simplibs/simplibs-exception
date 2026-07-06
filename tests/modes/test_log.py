from simplibs.exception.modes.LOG import LOG
from simplibs.exception.SimpleExceptionData import SimpleExceptionData

UNSET = SimpleExceptionData().value


class _StubData:
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


def test_render_produces_single_flat_line():
    result = LOG.render(_StubData(), validate=False)
    assert "\n" not in result


def test_render_includes_all_populated_fields():
    result = LOG.render(_StubData(), validate=False)
    assert "error='ERROR' label='my-label'" in result
    assert "message='my message'" in result
    assert "expected='expected thing'" in result
    assert "value=42 type=int" in result
    assert "problem='the problem'" in result
    assert "context='the context'" in result


def test_render_omits_missing_optional_fields():
    class _MinimalData:
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

    result = LOG.render(_MinimalData(), validate=False)
    assert result == "error=ERROR"


def test_singleton_repr():
    assert repr(LOG) == "<LogMessage mode>"
