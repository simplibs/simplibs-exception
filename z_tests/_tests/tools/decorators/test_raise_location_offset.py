"""
Tests for raise_location_offset decorator — metadata preservation, offset logic, and fallback.
"""
import pytest
from simplibs.exception.tools.decorators.raise_location_offset import raise_location_offset


class MockExceptionWithOffset(Exception):
    def __init__(self):
        self.called_with = None

    def with_location_offset(self, offset):
        self.called_with = offset
        return self


# -----------------------------------------------------------------------------
# Metadata preservation
# -----------------------------------------------------------------------------

def test_decorator_preserves_function_metadata():
    """The decorator must preserve __name__ and __doc__ of the original function."""
    @raise_location_offset(offset=1)
    def my_function():
        """Original docstring."""
        pass

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "Original docstring."


# -----------------------------------------------------------------------------
# Offset logic (Duck typing)
# -----------------------------------------------------------------------------

def test_decorator_calls_with_location_offset_on_exception():
    """If decorated function raises a SimpleException-like object, offset must be applied."""
    test_exc = MockExceptionWithOffset()

    @raise_location_offset(offset=5)
    def failing_func():
        raise test_exc

    with pytest.raises(MockExceptionWithOffset):
        failing_func()

    assert test_exc.called_with == 5


def test_decorator_suppresses_context_on_reraise():
    """Re-raised exception must have __cause__ and __context__ set to None (from None logic)."""
    @raise_location_offset(offset=1)
    def failing_func():
        raise MockExceptionWithOffset()

    with pytest.raises(MockExceptionWithOffset) as exc_info:
        failing_func()

    assert exc_info.value.__cause__ is None
    assert exc_info.value.__suppress_context__ is True


# -----------------------------------------------------------------------------
# Fallback logic (Standard exceptions)
# -----------------------------------------------------------------------------

def test_decorator_falls_back_for_standard_exceptions():
    """Standard exceptions without the offset method should be re-raised unchanged."""
    @raise_location_offset(offset=1)
    def failing_func():
        raise ValueError("Standard error")

    with pytest.raises(ValueError, match="Standard error"):
        failing_func()


# -----------------------------------------------------------------------------
# Success path
# -----------------------------------------------------------------------------

def test_decorator_does_not_interfere_with_successful_calls():
    """If no exception occurs, the decorator must return the function's result normally."""
    @raise_location_offset(offset=1)
    def success_func(a, b):
        return a + b

    assert success_func(10, 5) == 15