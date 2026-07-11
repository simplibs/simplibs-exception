"""
Tests for assert_exception_fields — attribute filtering, type matching, and sentinel evaluation.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.testing.asserts.asserts_fields.assert_exception_fields import assert_exception_fields


# -----------------------------------------------------------------------------
# Test Target Dummies & Mocks
# -----------------------------------------------------------------------------

class DummyExceptionDouble:
    """Mock container capturing all telemetry attributes expected by the field auditor."""

    def __init__(self) -> None:
        self.error_name = "AUDIT_ERROR"
        self.label = "auth-service"
        self.message = "Access denied"
        self.expected = "valid token"
        self.value = "expired token"
        self.problem = "Token verification failed"
        self.context = ("ip: 127.0.0.1", "port: 443")
        self.how_to_fix = "Refresh token"
        self.exception = None
        self.get_location = True
        self.skip_locations = ("simplibs.internal",)
        self.oneline = False


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

def test_asserts_only_specified_fields_and_ignores_unset_sentinels():
    """Verify that only parameters not equal to UNSET are actively audited on the target object."""
    exc = DummyExceptionDouble()
    spy = SubtestNoOpSpy()

    # Pass only a subset of attributes — others are UNSET and should not trigger assertion lookups
    result = assert_exception_fields(
        spy, exc,
        error_name="AUDIT_ERROR",
        label="auth-service",
        value="expired token"
    )

    assert result is exc  # Fluid API check: must return the target exception instance


def test_textual_field_evaluation_via_compare_strings_success_and_failure():
    """Verify that string attributes evaluate correctly using the underlying comparison engine."""
    exc = DummyExceptionDouble()
    spy = SubtestNoOpSpy()

    # 1. String success via partial fuzzy match
    assert_exception_fields(spy, exc, message="Access", exact_match=False)

    # 2. String failure via exact match mismatch
    with pytest.raises(AssertionError):
        assert_exception_fields(spy, exc, message="Access", exact_match=True)

    # 3. Tuple string sequence match
    assert_exception_fields(spy, exc, context=("ip: 127.0.0.1", "port: 443"), exact_match=True)


def test_primitive_and_structural_direct_assertions():
    """Verify that non-string attributes (booleans, exceptions, tuples) match strictly via standard equality."""
    exc = DummyExceptionDouble()
    spy = SubtestNoOpSpy()

    # 1. Boolean matching
    assert_exception_fields(spy, exc, get_location=True, oneline=False)
    with pytest.raises(AssertionError):
        assert_exception_fields(spy, exc, get_location=False)

    # 2. Structural tuple matching
    assert_exception_fields(spy, exc, skip_locations=("simplibs.internal",))
    with pytest.raises(AssertionError):
        assert_exception_fields(spy, exc, skip_locations=("other.package",))

    # 3. Embedded exception object matching
    assert_exception_fields(spy, exc, exception=None)
    with pytest.raises(AssertionError):
        assert_exception_fields(spy, exc, exception=ValueError())