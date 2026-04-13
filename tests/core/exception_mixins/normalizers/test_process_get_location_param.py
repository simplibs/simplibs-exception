"""
Tests for ProcessGetLocationParamMixin — direct pass-through and fallback to settings.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.core._exception_mixins.normalizers.ProcessGetLocationParam import ProcessGetLocationParamMixin
from simplibs.exception.core.SimpleExceptionSettings import SimpleExceptionSettings as S


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockData(ProcessGetLocationParamMixin):
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
# Valid values — direct pass-through
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("value", [0, 1, 2, 10])
def test_int_value_is_returned_directly(processor, value):
    """An int value must be returned directly without modification."""
    assert processor._process_get_location_param(value) == value


@pytest.mark.parametrize("value", [True, False])
def test_bool_value_is_returned_directly(processor, value):
    """A bool value must be returned directly without modification."""
    assert processor._process_get_location_param(value) is value


# -----------------------------------------------------------------------------
# Fallback to settings
# -----------------------------------------------------------------------------

def test_unset_returns_settings_default(processor):
    """UNSET must return S.DEFAULT_GET_LOCATION."""
    assert processor._process_get_location_param(UNSET) == S.DEFAULT_GET_LOCATION


@pytest.mark.parametrize("value", [None, "1", 1.5])
def test_invalid_input_returns_settings_default(processor, value):
    """Invalid inputs must return S.DEFAULT_GET_LOCATION."""
    assert processor._process_get_location_param(value) == S.DEFAULT_GET_LOCATION


def test_respects_live_settings_value(processor):
    """The method must read settings live — a change to settings must take effect immediately."""
    S.DEFAULT_GET_LOCATION = 5
    assert processor._process_get_location_param(UNSET) == 5