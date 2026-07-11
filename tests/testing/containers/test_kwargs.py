"""
Tests for Kwargs — initialization variants, mapping API integrity, and dictionary polymorphism.
"""
import pytest
from simplibs.exception._core_logic.internal_exceptions import SimpleExceptionSettingsError
from simplibs.exception.testing.containers.Kwargs import Kwargs


# -----------------------------------------------------------------------------
# Initialization Variations
# -----------------------------------------------------------------------------

def test_initialization_via_inline_kwargs():
    """Verify that passing explicit named parameters populates the internal dictionary."""
    kw = Kwargs(strict=True, timeout=30, mode="test")
    assert kw["strict"] is True
    assert kw["timeout"] == 30
    assert kw["mode"] == "test"


def test_initialization_via_single_dict_mapping():
    """Verify that passing a single positional mapping argument populates the wrapper."""
    kw = Kwargs({"strict": False, "retries": 3})
    assert kw["strict"] is False
    assert kw["retries"] == 3


def test_initialization_via_combined_dict_and_inline_kwargs():
    """Verify that inline kwargs override or append to the base dictionary mapping pass."""
    kw = Kwargs({"a": 1, "b": 2}, b=99, c=3)
    assert kw["a"] == 1
    assert kw["b"] == 99  # Overwritten by inline kwarg
    assert kw["c"] == 3  # Added by inline kwarg


def test_malformed_initialization_delegates_to_validation_raiser():
    """Verify that invalid initialization signatures trip the expected validation error."""
    # Passing multiple positional mappings
    with pytest.raises(SimpleExceptionSettingsError):
        Kwargs({"a": 1}, {"b": 2})

    # Passing a non-mapping primitive type
    with pytest.raises(SimpleExceptionSettingsError):
        Kwargs("invalid-type")


# -----------------------------------------------------------------------------
# Mapping API & Dunder Method Integrity
# -----------------------------------------------------------------------------

def test_mapping_protocol_compliance():
    """Verify length tracking, iteration capabilities, and item retrieval behaviors."""
    kw = Kwargs(x=10, y=20)

    # __len__
    assert len(kw) == 2

    # __iter__ / dictionary conversion conversion
    assert dict(kw) == {"x": 10, "y": 20}

    # __getitem__ access and missing key behavior
    assert kw["x"] == 10
    with pytest.raises(KeyError):
        _ = kw["missing_key"]


def test_immutability_and_frozen_nature():
    """Verify that the container enforces a read-only frozen interface."""
    kw = Kwargs(frozen=True)

    with pytest.raises(TypeError):
        # noinspection PyUnsupportedFeatures
        kw["frozen"] = False  # Immutable mapping cannot be mutated


def test_repr_rendering():
    """Verify that the string representation matches standard debugging expectations."""
    kw = Kwargs(a=1)
    assert repr(kw) == "Kwargs({'a': 1})"