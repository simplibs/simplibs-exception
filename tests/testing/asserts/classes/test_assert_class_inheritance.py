"""
Tests for assert_class_inheritance — verification of mandatory base class inheritance contracts.
"""
import pytest
from typing import Any
from simplibs.exception.SimpleExceptionData import SimpleExceptionData
from simplibs.exception.testing.asserts.asserts_classes.assert_class_inheritance import assert_class_inheritance


# -----------------------------------------------------------------------------
# Test Target Dummies & Mocks
# -----------------------------------------------------------------------------

class CompliantException(SimpleExceptionData, Exception):
    """A compliant exception architecture matching both inheritance constraints."""
    pass


class NativeOnlyException(Exception):
    """Non-compliant: inherits from native Exception but misses framework data layer."""
    pass


class NotAnException:
    """Non-compliant: a standard python class object completely foreign to error hierarchies."""
    pass


class SubtestNoOpSpy:
    """Zero-overhead dummy tracking stub satisfying subtests contract parameters."""
    def test(self, name: str):
        return self
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_inheritance_passes_for_fully_compliant_framework_exception():
    """Verify that a class inheriting from both BaseException and SimpleExceptionData passes cleanly."""
    spy = SubtestNoOpSpy()

    # Trigger inheritance matrix gate check
    result = assert_class_inheritance(spy, CompliantException, verbose=False)

    # Fluid API check: must return the checked class reference itself
    assert result is CompliantException


def test_inheritance_fails_for_native_only_exceptions():
    """Verify that validation fails if the class misses the framework SimpleExceptionData layer."""
    spy = SubtestNoOpSpy()

    # Must raise AssertionError on step 2 (SimpleExceptionData alignment check)
    with pytest.raises(AssertionError):
        assert_class_inheritance(spy, NativeOnlyException, verbose=False)


def test_inheritance_fails_for_arbitrary_non_exception_types():
    """Verify that a standard object class completely trips the baseline hierarchy guardrail."""
    spy = SubtestNoOpSpy()

    # Must raise AssertionError right on step 1 (BaseException alignment check)
    with pytest.raises(AssertionError):
        assert_class_inheritance(spy, NotAnException, verbose=False)