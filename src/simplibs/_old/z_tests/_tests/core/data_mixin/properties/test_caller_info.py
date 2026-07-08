"""
Tests for CallerInfo mixin — lazy loading, caching, and parameter passing.
Based on the actual src/simplibs/exception structure.
"""
import pytest
from unittest.mock import patch
from simplibs.sentinels import UNSET
from simplibs.exception.core._data_mixin.properties.CallerInfo import CallerInfoMixin


class MockData(CallerInfoMixin):
    """Fake data object simulating SimpleExceptionData with required attributes."""
    def __init__(self, get_location=1, skip_locations=()):
        self._get_location = get_location
        self._skip_locations = skip_locations
        self._cached_caller_info = UNSET


# -----------------------------------------------------------------------------
# Lazy Evaluation & Caching
# -----------------------------------------------------------------------------

def test_caller_info_is_computed_lazily():
    """The introspection logic must not run until caller_info is accessed."""
    # Patch the utility where CallerInfo imports it
    target = "simplibs.exception.core._data_mixin.properties.CallerInfo.extract_caller_info"
    with patch(target) as mock_extract:
        mock_extract.return_value = {"file": "test.py"}

        obj = MockData()
        # No call should have been made yet
        assert mock_extract.call_count == 0

        # First access triggers the computation
        info = obj.caller_info
        assert info == {"file": "test.py"}
        assert mock_extract.call_count == 1


def test_caller_info_caching():
    """Subsequent accesses must return the cached value without re-computing."""
    target = "simplibs.exception.core._data_mixin.properties.CallerInfo.extract_caller_info"
    with patch(target) as mock_extract:
        mock_extract.return_value = {"file": "test.py"}

        obj = MockData()

        # Multiple accesses
        _ = obj.caller_info
        _ = obj.caller_info
        _ = obj.caller_info

        # Must be called only once thanks to caching
        assert mock_extract.call_count == 1


# -----------------------------------------------------------------------------
# Parameter Passing
# -----------------------------------------------------------------------------

def test_parameters_passed_correctly_to_utility():
    """The mixin must pass _get_location directly as expected_frames (no +1)."""
    target = "simplibs.exception.core._data_mixin.properties.CallerInfo.extract_caller_info"
    with patch(target) as mock_extract:
        skip_patterns = ("pattern1", "pattern2")
        obj = MockData(get_location=3, skip_locations=skip_patterns)

        _ = obj.caller_info

        # Verify that the exact value from _get_location is passed
        mock_extract.assert_called_once_with(
            expected_frames=3,
            excluded_patterns=skip_patterns
        )


# -----------------------------------------------------------------------------
# Location Reporting Disabled (Fallbacks)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("disabled_value", [False, 0])
def test_returns_none_when_location_is_disabled(disabled_value):
    """If _get_location is False or 0, return None without calling utility."""
    target = "simplibs.exception.core._data_mixin.properties.CallerInfo.extract_caller_info"
    with patch(target) as mock_extract:
        obj = MockData(get_location=disabled_value)

        result = obj.caller_info

        assert result is None
        assert mock_extract.call_count == 0
        # Cache must contain None
        assert obj._cached_caller_info is None


# -----------------------------------------------------------------------------
# Failure Resilience
# -----------------------------------------------------------------------------

def test_handles_utility_failure_gracefully():
    """If extract_caller_info returns None, the property should also be None."""
    target = "simplibs.exception.core._data_mixin.properties.CallerInfo.extract_caller_info"
    with patch(target) as mock_extract:
        mock_extract.return_value = None

        obj = MockData()
        assert obj.caller_info is None
        assert obj._cached_caller_info is None