"""
Tests for SimpleExceptionInternalError — inheritance, formatting, and group exception boundaries.
"""
import pytest
from dataclasses import dataclass
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import SimpleExceptionInternalError
from simplibs.exception.SimpleExceptionData import SimpleExceptionData


# -----------------------------------------------------------------------------
# Architectural Boundaries & Inheritance
# -----------------------------------------------------------------------------

def test_inheritance_hierarchy():
    """Verify that internal errors structurally group under SimpleExceptionData and Exception."""
    error = SimpleExceptionInternalError()
    assert isinstance(error, SimpleExceptionData)
    assert isinstance(error, Exception)


def test_default_identity_and_storage():
    """Verify default naming and that descriptive attributes are correctly retained."""
    error = SimpleExceptionInternalError(
        value="internal_payload",
        expected="stable_state",
        problem="subsystem_fault"
    )
    assert error.error_name == "INTERNAL ERROR"
    assert error.value == "internal_payload"
    assert error.expected == "stable_state"
    assert error.problem == "subsystem_fault"


# -----------------------------------------------------------------------------
# Post-Init Rendering Engine
# -----------------------------------------------------------------------------

def test_post_init_renders_via_pretty():
    """Verify that __post_init__ processes payload into a rich PRETTY text string inside Exception layer."""
    problem_text = "core loop failure"
    error = SimpleExceptionInternalError(problem=problem_text)

    rendered = str(error)

    # Verify it's a non-empty string populated with rich elements
    assert isinstance(rendered, str)
    assert "INTERNAL ERROR" in rendered
    assert problem_text in rendered
    assert "═══" in rendered  # Verifies PRETTY mode's double frames are applied


# -----------------------------------------------------------------------------
# Subclassing & Group Exception Trapping
# -----------------------------------------------------------------------------

@dataclass
class DummySettingsError(SimpleExceptionInternalError):
    error_name: str = "SETTINGS ERROR"


def test_subclass_behavior_and_trapping():
    """Verify that custom internal subclasses inherit rendering mechanics and are catchable via the base class."""
    sub_error = DummySettingsError(problem="invalid_key")

    # 1. Check custom identity override
    assert sub_error.error_name == "SETTINGS ERROR"
    assert "SETTINGS ERROR" in str(sub_error)

    # 2. Verify group exception catching works flawlessly
    with pytest.raises(SimpleExceptionInternalError):
        raise sub_error