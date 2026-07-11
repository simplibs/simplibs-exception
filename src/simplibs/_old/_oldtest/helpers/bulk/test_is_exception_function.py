"""
Tests for is_exception_function — structural signature validation for exception-function test pairs.
"""
from simplibs.exception.testing._helpers.bulk.is_exception_function import is_exception_function


# -----------------------------------------------------------------------------
# Test Target Dummies
# -----------------------------------------------------------------------------

def dummy_validator():
    pass


class DummyNotException:
    pass


# -----------------------------------------------------------------------------
# Test Cases
# -----------------------------------------------------------------------------

def test_matches_valid_exception_function_tuples():
    """Verify that compliant exception-callable tuple variations evaluate to True."""
    # Standard 2-item tuple: (ExceptionClass, Callable)
    assert is_exception_function((ValueError, dummy_validator)) is True
    assert is_exception_function((RuntimeError, lambda: None)) is True

    # Multi-item tuple containing extra parameters: (ExceptionClass, Callable, *args)
    assert is_exception_function((ValueError, dummy_validator, "param")) is True
    assert is_exception_function((TypeError, dummy_validator, 123, {"key": "val"})) is True


def test_rejects_invalid_tuple_structures():
    """Verify that tuples with wrong lengths or non-compliant element types evaluate to False."""
    # Empty or single-item tuples
    assert is_exception_function(()) is False
    assert is_exception_function((ValueError,)) is False

    # Index 0 is not an exception class
    assert is_exception_function((DummyNotException, dummy_validator)) is False
    assert is_exception_function(("ValueError", dummy_validator)) is False

    # Index 1 is not a callable object
    assert is_exception_function((ValueError, "not_a_function")) is False
    assert is_exception_function((ValueError, None)) is False


def test_rejects_non_tuple_items():
    """Verify that any non-tuple types evaluate to False immediately."""
    assert is_exception_function(ValueError) is False
    assert is_exception_function(dummy_validator) is False
    assert is_exception_function([ValueError, dummy_validator]) is False  # List is not allowed
    assert is_exception_function("flat_string") is False