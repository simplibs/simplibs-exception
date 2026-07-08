import pytest

from simplibs.sentinels import UNSET
from simplibs.exception.modes.LOG import LOG


class _StubData:
    """Mock structure with tuples to verify logfmt flattening for complex fields."""
    error_name = "ERROR"
    label = "my-label"
    message = "my message"
    expected = "expected thing"
    value = 42
    # Tuple inputs to test if LOG mode correctly flattens them via print_problem/print_context
    problem = ("Problem part 1", "Problem part 2")
    context = ("Context line 1", "Context line 2")
    how_to_fix = "fix it"
    caller_info = None
    exception = None


def test_render_produces_single_flat_line():
    result = LOG._render(_StubData())
    assert "\n" not in result


def test_render_includes_all_populated_fields():
    """Verifies that all tokens are correctly formatted and complex fields are flattened."""
    result = LOG._render(_StubData())

    # Assert primary structure
    assert "error='ERROR' label='my-label'" in result
    assert "message='my message'" in result
    assert "expected='expected thing'" in result

    # Opravený assert: očekáváme typ jako token bez uvozovek (int)
    assert "value=42 type=int" in result

    # Ověření, že se tuple prvky slily do jednoho řetězce a byly zabaleny do repr uvozovek
    assert "problem='Problem part 1 Problem part 2'" in result
    assert "context='Context line 1 Context line 2'" in result


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

    result = LOG._render(_MinimalData())
    assert result == "error='ERROR'"


def test_singleton_repr():
    assert repr(LOG) == "<LogMessage mode>"