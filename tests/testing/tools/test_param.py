"""
Tests for Param — initialization compliance, value isolation, and frozen layout guards.
"""
import pytest
from dataclasses import FrozenInstanceError
from simplibs.exception.testing.tools.Param import Param


def test_param_isolates_scalar_primitives():
    """Verify that Param cleanly stores and exposes standard atomic scalar payloads."""
    p = Param("test-string")
    assert p.value == "test-string"


def test_param_isolates_complex_sequences():
    """Verify that a sequence collection is captured as a singular raw literal value."""
    sequence_payload = ("a.py", "b.py")
    p = Param(sequence_payload)

    # Ensure the inner collection identity and structure are preserved exactly as-is
    assert p.value == sequence_payload
    assert len(p.value) == 2


def test_param_isolates_dictionary_mappings():
    """Verify that dictionary configurations are retained without accidental decomposition."""
    mapping_payload = {"strict": True, "depth": 2}
    p = Param(mapping_payload)

    assert p.value == mapping_payload
    assert p.value["strict"] is True


def test_param_immutability_and_frozen_nature():
    """Verify that the container layout is strictly frozen and blocks modification attempts."""
    p = Param(42)

    with pytest.raises(FrozenInstanceError):
        # noinspection PyUnsupportedFeatures
        p.value = 99  # Immutable slots attribute cannot be mutated


def test_repr_rendering():
    """Verify that the debugging representation explicitly exposes the internal token type."""
    p = Param(("a.py",))
    assert repr(p) == "Param(('a.py',))"