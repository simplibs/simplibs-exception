"""
Tests for deep_test_exception_class — architectural auditing, subclass integrity, and serialization checks.
"""
import pytest
from simplibs.exception.testing._helpers.bulk.deep_test_exception_class import deep_test_exception_class
from simplibs.exception.testing._helpers.assertions.check_exception_fields import check_exception_fields

# We need a dummy object that mimics SimpleExceptionData for issubclass verification.
# Since we are writing unit tests for the helper itself, we can mock or import it.
# To keep it completely independent, we can mock the module or match the expected class.
from simplibs.exception.testing._helpers.bulk.deep_test_exception_class import SimpleExceptionData


# -----------------------------------------------------------------------------
# Test Doubles & Mocks
# -----------------------------------------------------------------------------

class ValidExceptionDouble(SimpleExceptionData):
    """A perfectly compliant custom exception mockup satisfying all architectural contracts."""
    error_name = "VALID_DOUBLE"
    label = "System Test Boundary"

    def __init__(self, **kwargs):
        # Allow zero-argument init, and allow setting custom values for inner validations
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        return "Formatted Exception Message"

    def to_dict(self) -> dict:
        return {"error": self.error_name}

    def to_debug_dict(self) -> dict:
        return {"error": self.error_name, "debug": True}


class NonCompliantExceptionDouble:
    """A flawed exception mockup that violates inheritance contracts (doesn't inherit from SimpleExceptionData)."""
    pass


class SubtestSpy:
    """Mock mirroring pytest-subtests engine to track registered evaluation checkpoints."""
    def __init__(self):
        self.called_subtests = []

    def test(self, name):
        self.called_subtests.append(name)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_compliant_class_passes_all_audit_layers():
    """Verify that a well-formed class triggers subclass, renderer, and serialization checkpoints successfully."""
    spy = SubtestSpy()

    # Execute deep audit over the compliant double
    deep_test_exception_class(spy, ValidExceptionDouble, verbose=True)

    # 1. Verify that the final execution end gateway subtest was hit
    assert "ValidExceptionDouble::deep_test_end" in spy.called_subtests

    # 2. Verify that inner pipeline components (renderer, serializations) were audited
    assert "ValidExceptionDouble::test_renderer" in spy.called_subtests
    assert "ValidExceptionDouble::test_to_dict" in spy.called_subtests
    assert "ValidExceptionDouble::test_to_debug_dict" in spy.called_subtests

    # 3. Verify that reflection checks from assert_exception_class were triggered
    assert "ValidExceptionDouble::test_error_name" in spy.called_subtests
    assert "ValidExceptionDouble::test_label" in spy.called_subtests


def test_non_compliant_class_raises_assertion_error():
    """Verify that a class violating the structural hierarchy contract is immediately rejected."""
    spy = SubtestSpy()

    # NonCompliantExceptionDouble does not inherit from SimpleExceptionData -> must raise AssertionError
    with pytest.raises(AssertionError, match="violates architectural contract"):
        deep_test_exception_class(spy, NonCompliantExceptionDouble, verbose=True)