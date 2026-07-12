"""
Tests for Args — initialization variants, sequence API integrity, and positional polymorphism.
"""
import pytest
from simplibs.exception.testing.tools.Args import Args


# -----------------------------------------------------------------------------
# Initialization Variations
# -----------------------------------------------------------------------------

def test_initialization_with_no_arguments():
    """Verify that an empty initialization creates a valid, zero-length sequence."""
    arg_box = Args()
    assert len(arg_box) == 0
    assert tuple(arg_box) == ()


def test_initialization_via_inline_positional_arguments():
    """Verify that passing multiple inline comma-separated nodes populates the registry."""
    arg_box = Args(42, "test-string", None, [1, 2])
    assert arg_box[0] == 42
    assert arg_box[1] == "test-string"
    assert arg_box[2] is None
    assert arg_box[3] == [1, 2]


def test_initialization_with_enclosed_collections():
    """Verify that complex containers passed inside the arguments are preserved as literal single units."""
    arg_box = Args(("a.py", "b.py"), {"key": "value"})
    assert len(arg_box) == 2
    assert arg_box[0] == ("a.py", "b.py")  # Maintained as a raw nested tuple parameter
    assert arg_box[1] == {"key": "value"}


# -----------------------------------------------------------------------------
# Sequence API & Dunder Method Integrity
# -----------------------------------------------------------------------------

def test_sequence_protocol_compliance():
    """Verify length tracking, iteration capabilities, and item retrieval behaviors."""
    arg_box = Args("a", "b", "c")

    # __len__
    assert len(arg_box) == 3

    # __iter__ / sequence tracking conversion
    assert tuple(arg_box) == ("a", "b", "c")
    assert list(arg_box) == ["a", "b", "c"]

    # __getitem__ positive and negative index lookups
    assert arg_box[0] == "a"
    assert arg_box[-1] == "c"

    with pytest.raises(IndexError):
        _ = arg_box[99]


def test_sequence_slice_retrieval():
    """Verify that slicing operations successfully return standard slice sub-tuples."""
    arg_box = Args(0, 1, 2, 3, 4)

    # Verify standard python slice behavior
    assert arg_box[1:4] == (1, 2, 3)
    assert arg_box[:2] == (0, 1)
    assert arg_box[3:] == (3, 4)


def test_immutability_and_frozen_nature():
    """Verify that the container enforces a read-only frozen interface."""
    arg_box = Args("immutable-payload")

    with pytest.raises(TypeError):
        # noinspection PyUnsupportedFeatures
        arg_box[0] = "mutated-value"  # Immutable sequence cannot be mutated


def test_repr_rendering():
    """Verify that the string representation matches standard debugging expectations."""
    arg_box = Args(1, "two")
    assert repr(arg_box) == "Args(1, 'two')"