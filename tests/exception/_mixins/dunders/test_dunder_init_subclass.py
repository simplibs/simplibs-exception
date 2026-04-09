"""
Tests for DunderInitSubclassMixin — valid definitions, errors at class definition time, and cooperative inheritance.
"""
import pytest
from simplibs.exception.exception._mixins.dunders.InitSubclass import DunderInitSubclassMixin
from simplibs.exception.base import SimpleExceptionInternalError


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockBase(DunderInitSubclassMixin):
    """Simulates the base class — SimpleException in real use."""
    pass


# -----------------------------------------------------------------------------
# Valid definitions
# -----------------------------------------------------------------------------

def test_valid_child_definition_passes():
    """A correctly defined subclass must pass without raising."""
    class ValidError(MockBase):
        message = "Everything is fine"
        error_name = "VALID_ERR"


# -----------------------------------------------------------------------------
# Error at class definition time — not at instantiation
# -----------------------------------------------------------------------------

def test_error_is_raised_at_class_definition_time():
    """The error must occur at class definition time — on import, not on instantiation."""
    with pytest.raises(SimpleExceptionInternalError):
        class BadError(MockBase):
            mesage = "Typo"  # should be 'message'

    # If we reached this point, the class was never created — it cannot be instantiated
    assert "BadError" not in dir()


# -----------------------------------------------------------------------------
# Unknown attributes (typo)
# -----------------------------------------------------------------------------

def test_unknown_attribute_raises():
    """A typo in an attribute name must raise SimpleExceptionInternalError."""
    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        class BadError(MockBase):
            mesage = "Typo in attribute name"  # should be 'message'

    assert "unknown attributes" in exc_info.value.problem
    assert "mesage" in exc_info.value.value


# -----------------------------------------------------------------------------
# Wrong attribute type
# -----------------------------------------------------------------------------

def test_wrong_type_raises():
    """An attribute with the wrong type must raise SimpleExceptionInternalError."""
    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        class WrongTypeError(MockBase):
            error_name = 123  # should be str

    assert "incorrect type" in exc_info.value.problem
    assert "error_name" in exc_info.value.value_label


# -----------------------------------------------------------------------------
# Cooperative inheritance
# -----------------------------------------------------------------------------

def test_kwargs_are_passed_to_super():
    """The mixin must forward kwargs — cooperative inheritance must not be broken."""
    class Tracker:
        called = False
        received_arg = None

        def __init_subclass__(cls, my_arg=None, **kwargs):
            Tracker.called = True
            Tracker.received_arg = my_arg
            super().__init_subclass__(**kwargs)

    class MultiDerived(DunderInitSubclassMixin, Tracker, my_arg="hello"):
        pass

    assert Tracker.called is True
    assert Tracker.received_arg == "hello"