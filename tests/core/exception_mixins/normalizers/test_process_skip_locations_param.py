"""
Tests for ProcessSkipLocationsParamMixin — input normalisation and merging with the global blacklist.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.core._exception_mixins.normalizers.ProcessSkipLocationsParam import ProcessSkipLocationsParamMixin
from simplibs.exception.core.SimpleExceptionSettings import SimpleExceptionSettings as S


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockData(ProcessSkipLocationsParamMixin):
    pass


@pytest.fixture
def processor():
    return MockData()


@pytest.fixture(autouse=True)
def reset_settings():
    S.reset()
    yield
    S.reset()


# -----------------------------------------------------------------------------
# Step 1 — input normalisation
# -----------------------------------------------------------------------------

def test_string_is_normalized_to_tuple(processor):
    """A string must be normalised to a single-element tuple."""
    result = processor._process_skip_locations_param("my_file.py")
    assert result == ("my_file.py",) + S.DEFAULT_LOCATION_BLACKLIST


def test_tuple_is_preserved(processor):
    """A tuple of strings must be preserved and merged with the blacklist."""
    result = processor._process_skip_locations_param(("a.py", "b.py"))
    assert result == ("a.py", "b.py") + S.DEFAULT_LOCATION_BLACKLIST


def test_list_is_converted_to_tuple(processor):
    """A list must be converted to a tuple and merged with the blacklist."""
    result = processor._process_skip_locations_param(["a.py", "b.py"])
    assert result == ("a.py", "b.py") + S.DEFAULT_LOCATION_BLACKLIST


def test_non_string_items_are_filtered_out(processor):
    """Non-string items must be silently removed."""
    result = processor._process_skip_locations_param(("a.py", 42, None, "b.py"))
    assert "a.py" in result
    assert "b.py" in result
    assert 42 not in result
    assert None not in result


@pytest.mark.parametrize("value", [(), []])
def test_empty_collection_returns_only_blacklist(processor, value):
    """An empty collection must return only the blacklist."""
    assert processor._process_skip_locations_param(value) == S.DEFAULT_LOCATION_BLACKLIST


@pytest.mark.parametrize("value", [UNSET, None, 42])
def test_invalid_input_returns_only_blacklist(processor, value):
    """Invalid input must return only the blacklist."""
    assert processor._process_skip_locations_param(value) == S.DEFAULT_LOCATION_BLACKLIST


# -----------------------------------------------------------------------------
# Step 2 — merging with the blacklist
# -----------------------------------------------------------------------------

def test_result_always_includes_blacklist(processor):
    """The result must always contain the entries from DEFAULT_LOCATION_BLACKLIST."""
    S.DEFAULT_LOCATION_BLACKLIST = ("blacklisted.py",)
    result = processor._process_skip_locations_param("my_file.py")
    assert "my_file.py" in result
    assert "blacklisted.py" in result


def test_respects_live_settings_blacklist(processor):
    """The method must read the blacklist live — a change to settings must take effect immediately."""
    S.DEFAULT_LOCATION_BLACKLIST = ("dynamic.py",)
    result = processor._process_skip_locations_param(UNSET)
    assert result == ("dynamic.py",)