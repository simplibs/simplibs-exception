import pytest

from simplibs.sentinels import UNSET
from simplibs.exception.modes.ONELINE import ONELINE


class _StubData:
    """Mock structure with multi-line tuples to verify flattening and layout integrity."""
    error_name = "ERROR"
    label = "my-label"
    message = "my message"
    expected = "expected thing"
    value = 42
    # Tuple with multiple items to test flattening logic
    problem = ("Problem part 1", "Problem part 2")
    context = ("Context line 1", "Context line 2")
    how_to_fix = "fix it"
    caller_info = None
    exception = None


def test_render_flattens_tuples_horizontally():
    """
    Architectural Contract: Verifies that multi-line inputs (tuples) provided to
    problem/context fields are flattened into the horizontal pipe-separated stream,
    ensuring no physical newlines escape into the ONELINE output.
    """
    result = ONELINE._render(_StubData())

    # 1. Kontrola, že nikde není '\n' (fyzický zlom řádku)
    assert "\n" not in result

    # 2. Kontrola, že tuple prvky byly spojeny mezerou v rámci svého bloku
    # (vycházíme z implementace print_problem/print_context s _oneline=True)
    assert "Problem:   Problem part 1 Problem part 2" in result
    assert "Context:   Context line 1 Context line 2" in result

    # 3. Kontrola celkové pipe separace
    assert " | " in result


def test_render_includes_all_populated_fields():
    """Verifies that all components are correctly strung together."""
    result = ONELINE._render(_StubData())
    assert "⚠️ ERROR: my-label" in result
    assert "Message:   my message" in result
    assert "Got:       42 (int)" in result


def test_singleton_repr():
    assert repr(ONELINE) == "<OnelineMessage mode>"