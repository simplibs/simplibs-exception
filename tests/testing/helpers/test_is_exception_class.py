"""
Tests for is_exception_class — type guard evaluation for exception class blueprints.
"""
import pytest
from simplibs.exception.testing._helpers.is_exception_class import is_exception_class


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_matches_genuine_exception_classes():
    """Verify that raw exception classes (builtin or custom) correctly evaluate to True."""
    # Built-in exceptions
    assert is_exception_class(ValueError) is True
    assert is_exception_class(RuntimeError) is True
    assert is_exception_class(BaseException) is True

    # Custom exceptions
    class CustomError(Exception):
        pass
    assert is_exception_class(CustomError) is True


def test_rejects_exception_instances():
    """Verify that instantiated exception objects evaluate to False."""
    assert is_exception_class(ValueError("mismatch")) is False
    assert is_exception_class(RuntimeError()) is False


def test_rejects_non_exception_types_and_primitives():
    """Verify that arbitrary standard types, functions, and primitive scalars evaluate to False."""
    # Standard classes/types
    assert is_exception_class(str) is False
    assert is_exception_class(dict) is False
    assert is_exception_class(object) is False

    # Functions / Callables
    def dummy_func():
        pass
    assert is_exception_class(dummy_func) is False

    # Primitives / Scalars / Sentinels
    assert is_exception_class("ValueError") is False
    assert is_exception_class(42) is False
    assert is_exception_class(None) is False