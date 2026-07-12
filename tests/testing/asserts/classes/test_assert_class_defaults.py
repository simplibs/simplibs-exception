"""
Tests for assert_class_defaults — reflection-driven auditing of static class metadata fallback.
"""
import pytest
from typing import Any
from simplibs.exception.testing.asserts.classes.assert_class_defaults import assert_class_defaults

# -----------------------------------------------------------------------------
# Test Target Dummies & Mocks
# -----------------------------------------------------------------------------

class CompliantDefaultsMock(Exception):
    """A compliant exception declaring class-level defaults that map cleanly to instances."""
    error_name = "DEFAULT_ERROR"
    label = "system-core"
    get_location = True

    def __init__(self) -> None:
        super().__init__()
        # Simulating standard framework behavior where class attributes are visible on instance


class BrokenDefaultsMock(Exception):
    """A broken class where initialization sabotages or overwrites class-declared defaults."""
    error_name = "CRITICAL_FAILURE"
    label = "database"

    def __init__(self) -> None:
        super().__init__()
        # Structural Malfunction Simulation: Clear out or mutate the default value during init
        self.error_name = "MUTATED_VALUE_DURING_INIT"


class SubtestNoOpSpy:
    """Zero-overhead dummy tracking stub satisfying subtests contract parameters."""
    def test(self, name: str):
        return self
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_class_defaults_pass_for_compliant_metadata_mapping():
    """Verify that class-level constants match instance values perfectly."""
    spy = SubtestNoOpSpy()

    # Trigger default fallback reflection check
    result = assert_class_defaults(spy, CompliantDefaultsMock, verbose=False)

    # Fluid API check: must return the instantiated and validated object
    assert isinstance(result, CompliantDefaultsMock)
    assert result.error_name == "DEFAULT_ERROR"
    assert result.label == "system-core"


def test_class_defaults_fail_if_initialization_mutates_class_constants():
    """Verify that any variance between declared class constants and instance layout triggers failure."""
    spy = SubtestNoOpSpy()

    # The audit must catch that the instance mutated 'error_name' away from 'CRITICAL_FAILURE'
    with pytest.raises(AssertionError):
        assert_class_defaults(spy, BrokenDefaultsMock, verbose=False)