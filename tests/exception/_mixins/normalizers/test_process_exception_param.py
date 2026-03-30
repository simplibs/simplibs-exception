"""
Tests for ProcessExceptionParamMixin — class-level default, exception classes, instances, and invalid inputs.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.exception._mixins.normalizers.ProcessExceptionParam import ProcessExceptionParamMixin


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockData(ProcessExceptionParamMixin):
    exception = UNSET


@pytest.fixture
def processor():
    return MockData()


# -----------------------------------------------------------------------------
# Step 1 — class-level default
# -----------------------------------------------------------------------------

def test_unset_without_class_default_returns_unset(processor):
    """UNSET with no class-level default must return (UNSET, UNSET)."""
    assert processor._process_exception_param(UNSET) == (UNSET, UNSET)


def test_unset_with_class_default_uses_default():
    """UNSET with a class-level default must use the value from the class."""
    class MockWithDefault(ProcessExceptionParamMixin):
        exception = ValueError

    exc_type, desc = MockWithDefault()._process_exception_param(UNSET)
    assert exc_type is ValueError
    assert desc is UNSET


# -----------------------------------------------------------------------------
# Step 2 — exception class
# -----------------------------------------------------------------------------

def test_exception_class_returns_class_and_unset_desc(processor):
    """Passing an exception class must return the class and UNSET as the description."""
    exc_type, desc = processor._process_exception_param(ValueError)
    assert exc_type is ValueError
    assert desc is UNSET


def test_non_exception_class_returns_unset(processor):
    """A class that does not inherit from Exception must return (UNSET, UNSET)."""
    class NotAnError:
        pass

    assert processor._process_exception_param(NotAnError) == (UNSET, UNSET)


# -----------------------------------------------------------------------------
# Step 3 — exception instance
# -----------------------------------------------------------------------------

def test_exception_instance_with_message_returns_type_and_desc(processor):
    """An exception instance with a message must return the type and the message as description."""
    exc_type, desc = processor._process_exception_param(RuntimeError("Something went wrong"))
    assert exc_type is RuntimeError
    assert desc == "Something went wrong"


def test_exception_instance_without_message_returns_unset_desc(processor):
    """An exception instance without a message must return the type and UNSET as description."""
    exc_type, desc = processor._process_exception_param(ValueError())
    assert exc_type is ValueError
    assert desc is UNSET


# -----------------------------------------------------------------------------
# Step 4 — invalid inputs
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("value", [None, "Not an exception", 42])
def test_invalid_inputs_return_unset(processor, value):
    """Invalid inputs must return (UNSET, UNSET)."""
    assert processor._process_exception_param(value) == (UNSET, UNSET)