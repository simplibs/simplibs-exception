"""
Tests for TestCase — declarative scenario storage and execution proxy routing.
"""
import pytest
import sys
from typing import Any
from simplibs.sentinels import UNSET
from simplibs.exception.testing.bulk_test.FunctionCase import FunctionCase


# -----------------------------------------------------------------------------
# Test Target Dummies & Mocks
# -----------------------------------------------------------------------------

def dummy_logic_gate():
    """Target business logic routine under test."""
    pass


class MockException(Exception):
    """Target exception blueprint to intercept."""
    pass


class AssertFunctionSpy:
    """Spy replacing the global assert_exception_function engine to track intercepted keywords."""

    def __init__(self) -> None:
        self.called_kwargs = {}

    def __call__(self, subtests: Any, func: Any, **kwargs: Any) -> MockException:
        self.called_kwargs = kwargs
        # Combine given function and subtests into tracker for verification if needed
        self.called_kwargs["_subtests"] = subtests
        self.called_kwargs["_func"] = func
        return MockException("Intercepted live exception double")


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_function_case_stores_and_decouples_static_expectation_blueprint():
    """Verify that the dataclass correctly mounts all declarative attributes and defaults."""
    case = FunctionCase(
        func=dummy_logic_gate,
        exception_type=MockException,
        label="io-subsystem",
        error_name="STORAGE_ERROR",
        valid_param={"mode": "safe"}
    )

    # Core required fields
    assert case.func is dummy_logic_gate
    assert case.exception_type is MockException

    # Manually assigned metadata fields
    assert case.label == "io-subsystem"
    assert case.error_name == "STORAGE_ERROR"
    assert case.valid_param == {"mode": "safe"}

    # Default sentinel fields must remain UNSET
    assert case.invalid_param is UNSET
    assert case.message is UNSET
    assert case.problem is UNSET
    assert case.how_to_fix is UNSET


def test_run_test_proxies_entire_payload_down_to_assertion_engine(monkeypatch):
    """Verify that run_test seamlessly unpacks and forwards properties to assert_exception_function."""
    spy = AssertFunctionSpy()

    # -------------------------------------------------------------------------
    # Namespace Interception (Monkeypatch Setup)
    # -------------------------------------------------------------------------
    # Resolve the underlying module object dynamically via sys.modules.
    # This bypasses namespace collisions where the local 'FunctionCase' identifier
    # refers to the dataclass type rather than the raw module container.
    module = sys.modules[FunctionCase.__module__]

    # Intercept the localized assertion function inside the target module
    monkeypatch.setattr(
        module,
        "assert_exception_function",
        spy,
    )

    # -------------------------------------------------------------------------
    # Scenario Configuration & Execution
    # -------------------------------------------------------------------------
    case = FunctionCase(
        func=dummy_logic_gate,
        exception_type=MockException,
        label="network-layer",
        error_name="TIMEOUT",
        expected="active connection",
        value="disconnected"
    )

    fake_subtests_manager = "pytest-subtests-fixture-instance"

    # Trigger execution routing block to proxy the payload downstream
    live_exc = case.run_test(
        subtests=fake_subtests_manager,
        exact_match=False,
        verbose=True,
        intro="prefix::",
        deep_check=False
    )

    # -------------------------------------------------------------------------
    # Assertions & Verification
    # -------------------------------------------------------------------------
    # Verify return value matches downstream engine payload mapping
    assert isinstance(live_exc, MockException)

    # Validate that all structured declarative properties were delegated correctly
    assert spy.called_kwargs["_subtests"] == "pytest-subtests-fixture-instance"
    assert spy.called_kwargs["_func"] is dummy_logic_gate
    assert spy.called_kwargs["exception_type"] is MockException
    assert spy.called_kwargs["label"] == "network-layer"
    assert spy.called_kwargs["error_name"] == "TIMEOUT"
    assert spy.called_kwargs["expected"] == "active connection"
    assert spy.called_kwargs["value"] == "disconnected"

    # Validate runtime execution settings orchestration flags
    assert spy.called_kwargs["exact_match"] is False
    assert spy.called_kwargs["verbose"] is True
    assert spy.called_kwargs["intro"] == "prefix::"
    assert spy.called_kwargs["deep_check"] is False