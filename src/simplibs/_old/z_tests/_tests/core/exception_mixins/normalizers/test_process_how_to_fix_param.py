"""
Tests for ProcessHowToFixParamMixin — string wrapping, tuple/list normalisation, and fallback to class defaults.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.core._exception_mixins.normalizers.ProcessHowToFixParam import ProcessHowToFixParamMixin


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockData(ProcessHowToFixParamMixin):
    how_to_fix = ("Default fix",)


@pytest.fixture
def processor():
    return MockData()


# -----------------------------------------------------------------------------
# Step 1 — string
# -----------------------------------------------------------------------------

def test_string_is_wrapped_in_tuple(processor):
    """A single string must be wrapped in a tuple."""
    assert processor._process_how_to_fix_param("Fix it") == ("Fix it",)


# -----------------------------------------------------------------------------
# Step 2 — tuple and list
# -----------------------------------------------------------------------------

def test_valid_tuple_is_preserved(processor):
    """A valid tuple must be returned as a tuple."""
    result = processor._process_how_to_fix_param(("Fix A", "Fix B"))
    assert result == ("Fix A", "Fix B")
    assert isinstance(result, tuple)


def test_list_is_converted_to_tuple(processor):
    """A list must be accepted and converted to a tuple."""
    result = processor._process_how_to_fix_param(["Fix A", "Fix B"])
    assert result == ("Fix A", "Fix B")
    assert isinstance(result, tuple)


def test_non_string_items_are_filtered_out(processor):
    """Non-string items must be silently removed."""
    result = processor._process_how_to_fix_param(("Valid", 123, None, "Also valid"))
    assert result == ("Valid", "Also valid")


# -----------------------------------------------------------------------------
# Step 3 — fallback to class-level default
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("value", [(), []])
def test_empty_collection_falls_back_to_default(processor, value):
    """An empty collection must return the class-level default."""
    assert processor._process_how_to_fix_param(value) == ("Default fix",)


@pytest.mark.parametrize("value", [None, 42, UNSET])
def test_invalid_input_falls_back_to_default(processor, value):
    """Invalid input must return the class-level default."""
    assert processor._process_how_to_fix_param(value) == ("Default fix",)


def test_unset_class_default_returns_unset():
    """If the class-level default is UNSET, UNSET must be returned."""
    class MockWithUnset(ProcessHowToFixParamMixin):
        how_to_fix = UNSET

    assert MockWithUnset()._process_how_to_fix_param(None) is UNSET


def test_subclass_default_has_priority():
    """The fallback must respect the subclass class-level default."""
    class CustomData(MockData):
        how_to_fix = ("Custom fix",)

    assert CustomData()._process_how_to_fix_param(None) == ("Custom fix",)