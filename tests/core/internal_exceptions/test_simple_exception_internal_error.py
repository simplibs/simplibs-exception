"""
Tests for SimpleExceptionInternalError — inheritance, initialization, and subclassing.
"""
import pytest
from dataclasses import dataclass
from simplibs.exception.core._internal_exceptions.SimpleExceptionInternalError import SimpleExceptionInternalError
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData


# -----------------------------------------------------------------------------
# Inheritance and Types
# -----------------------------------------------------------------------------

def test_inherits_from_simple_exception_data():
    """SimpleExceptionInternalError must inherit from SimpleExceptionData."""
    assert isinstance(SimpleExceptionInternalError(), SimpleExceptionData)


def test_inherits_from_exception():
    """SimpleExceptionInternalError must inherit from Exception."""
    assert isinstance(SimpleExceptionInternalError(), Exception)


def test_default_error_name():
    """Default error_name must be 'INTERNAL ERROR'."""
    assert SimpleExceptionInternalError().error_name == "INTERNAL ERROR"


# -----------------------------------------------------------------------------
# Initialization and Message
# -----------------------------------------------------------------------------

def test_custom_attributes_are_stored():
    """Data attributes passed at init must be stored correctly."""
    error = SimpleExceptionInternalError(
        value="bad_value",
        expected="good_value",
        problem="mismatch",
    )
    assert error.value == "bad_value"
    assert error.expected == "good_value"
    assert error.problem == "mismatch"


def test_str_returns_non_empty_string():
    """__post_init__ must render a non-empty message via PRETTY."""
    error = SimpleExceptionInternalError(problem="something went wrong")
    assert isinstance(str(error), str)
    assert len(str(error)) > 0


# -----------------------------------------------------------------------------
# Raise and Catch
# -----------------------------------------------------------------------------

def test_can_be_raised_and_caught():
    """Must be raiseable and catchable as a standard Exception."""
    with pytest.raises(SimpleExceptionInternalError):
        raise SimpleExceptionInternalError()


# -----------------------------------------------------------------------------
# Subclassing — Group Exceptions
# -----------------------------------------------------------------------------

@dataclass
class _SettingsError(SimpleExceptionInternalError):
    error_name: str = "SETTINGS ERROR"


def test_subclass_has_custom_error_name():
    """Subclass must override error_name correctly."""
    assert _SettingsError().error_name == "SETTINGS ERROR"


def test_subclass_is_instance_of_base():
    """Subclass instance must be catchable as SimpleExceptionInternalError."""
    assert isinstance(_SettingsError(), SimpleExceptionInternalError)


def test_subclass_can_be_caught_via_base_class():
    """Subclass must be catchable via except SimpleExceptionInternalError."""
    with pytest.raises(SimpleExceptionInternalError):
        raise _SettingsError(problem="bad config")