"""
Tests for raise_with_location_offset — duck typing check and fallback logic.
"""
import pytest
from unittest.mock import MagicMock
from simplibs.exception.tools.raise_with_location_offset import raise_with_location_offset


# -----------------------------------------------------------------------------
# Duck typing support (SimpleException-like objects)
# -----------------------------------------------------------------------------

def test_calls_with_location_offset_if_present():
    """If the exception has the method, it must be called with the provided offset."""
    mock_exc = MagicMock()
    mock_exc.with_location_offset.return_value = mock_exc

    with pytest.raises(Exception):
        raise_with_location_offset(mock_exc, offset=2)

    mock_exc.with_location_offset.assert_called_once_with(2)


def test_raises_the_returned_exception_from_offset_method():
    """It must raise the object returned by the with_location_offset method."""

    class CustomRaisedError(Exception): pass

    mock_exc = MagicMock()
    mock_exc.with_location_offset.return_value = CustomRaisedError("Shifted error")

    with pytest.raises(CustomRaisedError, match="Shifted error"):
        raise_with_location_offset(mock_exc)


# -----------------------------------------------------------------------------
# Fallback logic (Standard exceptions)
# -----------------------------------------------------------------------------

def test_raises_standard_exception_without_offset_method():
    """If the method is missing, it must raise the original exception normally."""
    standard_exc = ValueError("Standard error")

    with pytest.raises(ValueError, match="Standard error"):
        raise_with_location_offset(standard_exc)


# -----------------------------------------------------------------------------
# Default parameters
# -----------------------------------------------------------------------------

def test_default_offset_is_one():
    """If offset is not provided, it should default to 1."""
    mock_exc = MagicMock()
    mock_exc.with_location_offset.return_value = mock_exc

    with pytest.raises(Exception):
        raise_with_location_offset(mock_exc)

    mock_exc.with_location_offset.assert_called_once_with(1)