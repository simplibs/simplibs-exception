import pytest

from simplibs.exception.modes.ONELINE import ONELINE


class _StubData:
    """Mock structure providing fully populated exception fields for structural layout testing."""
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


def test_render_produces_pipe_separated_single_line():
    """
    Guarantees that the ONELINE layout engine flattens all metrics horizontally,
    separating segments using vertical pipes and strictly ensuring no newline characters
    are introduced.
    """
    # 1. Execute rendering engine on the stub data blueprint
    result = ONELINE.render(_StubData(), validate=False)

    # 2. Validate structural contract constraints
    assert "\n" not in result
    assert " | " in result


def test_render_includes_all_populated_fields():
    """
    Verifies that the horizontal formatter correctly processes and integrates
    every single populated field from the metadata snapshot, embedding the proper prefixes.
    """
    # 1. Execute rendering engine on the stub data blueprint
    result = ONELINE.render(_StubData(), validate=False)

    # 2. Assert that all standard data footprints are present in the serialized stream
    assert "⚠️ ERROR: my-label" in result
    assert "Message:   my message" in result
    assert "Expected:  expected thing" in result
    assert "Got:       42 (int)" in result
    assert "Problem:   the problem" in result
    assert "Context:   the context" in result


def test_singleton_repr():
    """Ensures the mode singleton instance provides a clean, recognizable debug string representation."""
    assert repr(ONELINE) == "<OnelineMessage mode>"