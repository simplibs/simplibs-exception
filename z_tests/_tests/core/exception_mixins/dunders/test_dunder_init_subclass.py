"""
Tests for DunderInitSubclassMixin — valid definitions, errors at class definition time, and cooperative inheritance.
Based on the actual src/simplibs/exception structure.
"""
import pytest
from unittest.mock import patch
from simplibs.exception.core._exception_mixins.dunders.InitSubclass import DunderInitSubclassMixin
from simplibs.exception.core._internal_exceptions.SimpleExceptionInternalError import SimpleExceptionInternalError
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData


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
    """A correctly defined subclass must pass without raising using real Data attributes."""
    # Using real attributes from SimpleExceptionData (error_name, message)
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
            mesage = "Typo"  # typo: mesage vs message

    # If the class were created, it would be in the local namespace.
    # However, pytest.raises catches the error before the definition completes.


# -----------------------------------------------------------------------------
# Integration with validation logic
# -----------------------------------------------------------------------------

def test_mixin_calls_validation_utility_with_correct_args():
    """The mixin must call check_children_class_attributes with SimpleExceptionData and the new class."""
    # Path to the utility within the Mixin
    target = "simplibs.exception.core._exception_mixins.dunders.InitSubclass.check_children_class_attributes"

    with patch(target) as mock_check:
        class TestClass(MockBase):
            pass

        # Verify that the mixin correctly linked Base (SimpleExceptionData) and the new class (TestClass)
        mock_check.assert_called_once_with(SimpleExceptionData, TestClass)


# -----------------------------------------------------------------------------
# Unknown attributes (typo)
# -----------------------------------------------------------------------------

def test_unknown_attribute_raises():
    """A typo in an attribute name must raise SimpleExceptionInternalError (via utility)."""
    with pytest.raises(SimpleExceptionInternalError) as exc_info:
        class BadError(MockBase):
            unknown_xyz = "Does not exist in SimpleExceptionData"

    assert "unknown attributes" in exc_info.value.problem
    assert "unknown_xyz" in exc_info.value.value


# -----------------------------------------------------------------------------
# Cooperative inheritance
# -----------------------------------------------------------------------------

def test_kwargs_are_passed_to_super():
    """The mixin must forward kwargs — cooperative inheritance must not be broken."""

    class Tracker:
        called = False
        received_arg = None

        @classmethod
        def __init_subclass__(cls, my_arg=None, **kwargs):
            Tracker.called = True
            Tracker.received_arg = my_arg
            super().__init_subclass__(**kwargs)

    # Important: DunderInitSubclassMixin must be in the MRO either before or after Tracker,
    # but both must cooperate via super().
    class MultiDerived(DunderInitSubclassMixin, Tracker, my_arg="hello"):
        pass

    assert Tracker.called is True
    assert Tracker.received_arg == "hello"