import pytest

from simplibs.sentinels import UNSET
from simplibs.exception.modes.SIMPLE import SIMPLE
from simplibs.exception.modes.printers.dividers.DOUBLE_LINE import DOUBLE_LINE


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
    """Architectural Contract: Ensures that the plain text mode strictly suppresses all graphic double-line dividers."""
    result = SIMPLE._render(_FullData())
    assert DOUBLE_LINE not in result


def test_render_includes_header_with_label():
    """Validates that the output opens directly with the primary identity header and its attached human label."""
    result = SIMPLE._render(_FullData())
    assert result.startswith("⚠️ ERROR: my-label")


def test_render_includes_all_populated_fields():
    """Verifies seamless integration: all granular structured metadata fields must be compiled and aligned properly."""
    result = SIMPLE._render(_FullData())
    assert "Message:   my message" in result
    assert "Expected:  expected thing" in result
    assert "Got:       42 (int)" in result
    assert "Problem:   the problem" in result
    assert "Context:   the context" in result
    assert "🔧 How to fix:" in result


def test_render_handles_empty_data_gracefully():
    """Confirms that the absolute minimum dataset generates a clean, single-line identity fallback without blank lines."""
    result = SIMPLE._render(_EmptyData())
    assert result == "⚠️ ERROR"


def test_singleton_repr():
    """Verifies that the stateless plain-text singleton instance exposes a clean, predictable string representation."""
    assert repr(SIMPLE) == "<SimpleMessage mode>"