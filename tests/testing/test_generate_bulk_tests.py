"""
Tests for generate_bulk_tests — orchestration, dynamic pipeline routing, and argument unpacking.
"""
import pytest
from simplibs.exception.testing.generate_bulk_tests import generate_bulk_tests
# We need the framework's contract base class for deep compliance test layer
from simplibs.exception.testing._helpers.bulk.deep_test_exception_class import SimpleExceptionData


# -----------------------------------------------------------------------------
# Test Doubles & Mocks
# -----------------------------------------------------------------------------

class CompliantExceptionDouble(SimpleExceptionData, Exception):
    """Compliant exception inheriting from Exception to pass core type guards."""
    error_name = "BULK_ERROR"

    def __str__(self) -> str:
        return "Bulk Exception Message"


def mock_flat_trigger() -> None:
    """Target function with no parameters that always raises the expected error."""
    raise CompliantExceptionDouble()


def mock_positional_trigger(a: int, b: str) -> None:
    """Target function expecting positional arguments."""
    if a < 0 or b == "invalid":
        raise CompliantExceptionDouble()


def mock_keyword_trigger(mode: str, strict: bool = False) -> None:
    """Target function expecting keyword-only or optional configurations."""
    if mode == "fail" and strict:
        raise CompliantExceptionDouble()


class SubtestSpy:
    """Mock mirroring pytest-subtests engine to track registered evaluation checkpoints."""
    def __init__(self):
        self.called_subtests = []

    def test(self, name):
        self.called_subtests.append(name)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


# -----------------------------------------------------------------------------
# Orchestrator Pipeline Tests
# -----------------------------------------------------------------------------

def test_shallow_mode_routing_matrix_success():
    """Verify routing over classes and various functional configurations under shallow mode."""
    spy = SubtestSpy()

    matrix_items = [
        # 1. Raw Exception Class (Shallow allocation check)
        CompliantExceptionDouble,
        # 2. Fixed invocation with zero parameters
        (CompliantExceptionDouble, mock_flat_trigger),
        # 3. Parametric routine with positional arguments
        (CompliantExceptionDouble, mock_positional_trigger, -1, "invalid"),
        # 4. Keyword argument unpacking via trailing dictionary
        (CompliantExceptionDouble, mock_keyword_trigger, "fail", {"strict": True}),
    ]

    generate_bulk_tests(spy, matrix_items, verbose=True, deep_exception_check=False)

    # Verify all distinct pipeline checkpoints were registered with their corresponding names
    assert "test_exc_class::CompliantExceptionDouble" in spy.called_subtests
    assert "test_exc_function::mock_flat_trigger" in spy.called_subtests
    assert "test_exc_function::mock_positional_trigger" in spy.called_subtests
    assert "test_exc_function::mock_keyword_trigger" in spy.called_subtests


def test_deep_mode_delegates_to_architectural_auditor():
    """Verify that deep_exception_check=True routes raw exception classes to deep checks."""
    spy = SubtestSpy()

    generate_bulk_tests(spy, [CompliantExceptionDouble], verbose=True, deep_exception_check=True)

    # Deep mode routes through deep_test_exception_class, registering its deep checkpoints
    assert "CompliantExceptionDouble::deep_test_end" in spy.called_subtests
    assert "CompliantExceptionDouble::test_renderer" in spy.called_subtests


def test_fallback_gate_rejects_unsupported_signatures():
    """Verify that any unrecognized or structurally malformed item triggers an AssertionError."""
    spy = SubtestSpy()

    # Lists are not recognized as valid functional sequence pairs (must be tuples)
    malformed_matrix = [
        [CompliantExceptionDouble, mock_flat_trigger]
    ]

    with pytest.raises(AssertionError, match="Unsupported item signature footprint"):
        generate_bulk_tests(spy, malformed_matrix, verbose=True)

    assert "unknown_item" in spy.called_subtests