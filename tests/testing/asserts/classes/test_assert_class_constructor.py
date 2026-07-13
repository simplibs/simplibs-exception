"""
Tests for assert_class_constructor — verification of constructor field propagation matrix and str() smoke paths.
"""
import pytest
from typing import Any
from simplibs.exception.testing.asserts.classes.assert_class_constructor import assert_class_constructor


# -----------------------------------------------------------------------------
# Test Target Dummies & Mocks
# -----------------------------------------------------------------------------

class CompliantExceptionMock(Exception):
    """A perfectly implemented exception class that stores all constructor inputs and satisfies str()."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        # Guarantee that the core diagnostic identities leak into the string output
        return f"⚠️ {getattr(self, 'error_name', '')} | Message: {getattr(self, 'message', '')}"


class BrokenExceptionMock(Exception):
    """An exception class that silently drops or mutates constructor arguments."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)
        # Structural Malfunction Simulation: Sabotage the label attribute
        self.label = "corrupted-value"

    def __str__(self) -> str:
        return f"⚠️ {getattr(self, 'error_name', '')} | Message: {getattr(self, 'message', '')}"


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

def test_constructor_propagation_passes_for_compliant_class():
    """Verify that a class accepting and storing the full parameter matrix passes cleanly."""
    spy = SubtestNoOpSpy()

    # Trigger full layout verification audit
    instance = assert_class_constructor(spy, CompliantExceptionMock, verbose=False)

    # Assert fluid API contract (returns the instantiated object)
    assert isinstance(instance, CompliantExceptionMock)
    assert instance.message == "<message>"
    assert instance.label == "<label>"


def test_constructor_propagation_fails_if_attributes_are_lost_or_mutated():
    """Verify that any internal truncation or mutation in the constructor trips the assertion."""
    spy = SubtestNoOpSpy()

    # The audit must detect that BrokenExceptionMock modified the 'label' field
    with pytest.raises(AssertionError):
        assert_class_constructor(spy, BrokenExceptionMock, verbose=False)