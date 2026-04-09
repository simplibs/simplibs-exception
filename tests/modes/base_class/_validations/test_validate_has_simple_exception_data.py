"""
Tests for validate_has_simple_exception_data and SimpleExceptionModeError — validation and error group.
"""
import pytest
from simplibs.exception.base import SimpleExceptionInternalError
from simplibs.exception.base.data.SimpleExceptionData import SimpleExceptionData
from simplibs.exception.modes.base_class._validations.SimpleExceptionModeError import SimpleExceptionModeError
from simplibs.exception.modes.base_class._validations.validate_has_simple_exception_data import validate_has_simple_exception_data


# -----------------------------------------------------------------------------
# validate_has_simple_exception_data
# -----------------------------------------------------------------------------

def test_passes_with_valid_data():
    """Must not raise when data is a SimpleExceptionData instance."""
    validate_has_simple_exception_data(SimpleExceptionData())


def test_passes_with_subclass():
    """Must accept subclasses of SimpleExceptionData."""
    class SubData(SimpleExceptionData):
        pass
    validate_has_simple_exception_data(SubData())


def test_raises_for_invalid_object():
    """Must raise SimpleExceptionModeError for objects that are not SimpleExceptionData."""
    invalid = "I am a string, not a dataclass"
    with pytest.raises(SimpleExceptionModeError) as exc_info:
        validate_has_simple_exception_data(invalid)
    assert exc_info.value.error_name == "MODE ERROR"
    assert exc_info.value.value == invalid
    assert "an instance of SimpleExceptionData" in exc_info.value.expected


# -----------------------------------------------------------------------------
# SimpleExceptionModeError
# -----------------------------------------------------------------------------

def test_mode_error_inherits_from_internal_error():
    """SimpleExceptionModeError must inherit from SimpleExceptionInternalError."""
    assert isinstance(SimpleExceptionModeError(), SimpleExceptionInternalError)


def test_mode_error_default_error_name():
    """Default error_name must be 'MODE ERROR'."""
    assert SimpleExceptionModeError().error_name == "MODE ERROR"