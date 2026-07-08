import pytest

from simplibs.sentinels import UNSET
from simplibs.exception.modes.PRETTY import PRETTY
from simplibs.exception.modes.printers.dividers.DOUBLE_LINE import DOUBLE_LINE
from simplibs.exception.modes.printers.dividers.SINGLE_LINE import SINGLE_LINE


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
    """Validates that the visual frame consistently opens with a full-width double line character buffer."""
    result = PRETTY._render(_FullData())
    lines = result.split("\n")
    assert lines[0] == DOUBLE_LINE


def test_render_includes_header_with_label():
    """Ensures that the primary identity section correctly renders both the identity name and its human label description."""
    result = PRETTY._render(_FullData())
    assert "⚠️ ERROR: my-label" in result


def test_render_includes_second_double_line_when_details_present():
    """
    Verifies elastic divider scaling: when dynamic details (expected, value, problem, context) 
    are populated, a secondary internal double-line divider must separate the header from the core body.
    """
    result = PRETTY._render(_FullData())
    # 3 lines expected: opening boundary + post-intro detail divider + closing boundary
    assert result.count(DOUBLE_LINE) == 3


def test_render_omits_second_double_line_when_no_details():
    """
    Ensures layout cleanliness: when granular comparison metadata is missing, 
    the engine must suppress the secondary body divider to prevent layout bloat.
    """
    result = PRETTY._render(_MessageOnlyData())
    # Only opening and closing lines should remain
    assert result.count(DOUBLE_LINE) == 2


def test_render_includes_single_line_before_how_to_fix():
    """Validates remediation formatting: actionable steps must be visually separated by a single-line divider block."""
    result = PRETTY._render(_FullData())
    assert SINGLE_LINE in result
    assert "🔧 How to fix:" in result


def test_render_omits_single_line_when_no_how_to_fix():
    """Guarantees that if no mitigation instructions are supplied, the single-line remediation separator is skipped."""
    result = PRETTY._render(_MessageOnlyData())
    assert SINGLE_LINE not in result


def test_render_handles_fully_empty_data_gracefully():
    """Confirms that the absolute minimum dataset successfully builds a valid, structurally coherent identity panel."""
    result = PRETTY._render(_EmptyData())
    assert "⚠️ ERROR" in result
    assert isinstance(result, str)


def test_render_includes_value_with_type():
    """Validates integration with underlying field printers, ensuring inspected values are accurately rendered with type markers."""
    result = PRETTY._render(_FullData())
    assert "Got:       42 (int)" in result


def test_singleton_repr():
    """Verifies that the stateless singleton instance exposes a clean, predictable string representation."""
    assert repr(PRETTY) == "<PrettyMessage mode>"


