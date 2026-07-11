"""
Tests for assert_class_interface — API contract verification for exception serialization and dunder methods.
"""
import pytest
from typing import Any
from simplibs.exception.testing.asserts.asserts_classes.assert_class_interface import assert_class_interface


# -----------------------------------------------------------------------------
# Test Target Dummies & Mocks
# -----------------------------------------------------------------------------

class CompliantInterfaceMock:
    """A mock exception matching the full public serialization API contract."""
    def __str__(self) -> str:
        return "Pretty Message"

    def __repr__(self) -> str:
        return "CompliantInterfaceMock()"

    def to_dict(self) -> dict[str, Any]:
        return {"error_name": "MOCK"}

    def to_debug_dict(self) -> dict[str, Any]:
        return {"error_name": "MOCK", "debug": True}

    def to_json(self) -> str:
        return '{"error_name": "MOCK"}'


class MissingMethodInterfaceMock(CompliantInterfaceMock):
    """Broken API: Deliberately omits the required 'to_json' method."""
    def __init__(self) -> None:
        # noinspection PyAttributeOutsideInit
        delattr(MissingMethodInterfaceMock, "to_json")


class BrokenTypeInterfaceMock(CompliantInterfaceMock):
    """Broken API: Method exists but violates type contract by returning an integer."""
    def to_dict(self) -> Any:
        return 12345  # Malfunction: Should return a dictionary


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

def test_interface_passes_for_fully_compliant_api_specification():
    """Verify that an object implementing all string and serialization methods passes cleanly."""
    spy = SubtestNoOpSpy()

    # Trigger public API validation check
    instance = assert_class_interface(spy, CompliantInterfaceMock, verbose=False)

    # Fluid API check: must return the instantiated and validated object
    assert isinstance(instance, CompliantInterfaceMock)


def test_interface_fails_if_required_method_is_missing():
    """Verify that omitting a mandatory API method like 'to_json' causes a failure."""
    spy = SubtestNoOpSpy()

    # Must raise AttributeError when step 5 attempts to invoke the missing to_json routine
    with pytest.raises(AttributeError):
        assert_class_interface(spy, MissingMethodInterfaceMock, verbose=False)


def test_interface_fails_if_method_returns_invalid_type():
    """Verify that a serialization method returning an unexpected primitive type trips the audit."""
    spy = SubtestNoOpSpy()

    # Must raise AssertionError when step 3 discovers that to_dict did not return a dict instance
    with pytest.raises(AssertionError):
        assert_class_interface(spy, BrokenTypeInterfaceMock, verbose=False)