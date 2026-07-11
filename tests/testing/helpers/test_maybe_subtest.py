"""
Tests for maybe_subtest — conditional pytest-subtests routing and execution paths.
"""
import pytest
from typing import Any
from simplibs.exception.testing._helpers.maybe_subtest import maybe_subtest


# -----------------------------------------------------------------------------
# Test Doubles & Mocks
# -----------------------------------------------------------------------------

class SubtestContextMock:
    """Mock representing the active inner subtest execution frame."""
    pass


class SubtestSpy:
    """Mock mirroring pytest-subtests fixture manager to verify execution lanes."""
    def __init__(self) -> None:
        self.called_with_name: str | None = None
        self.context_yielded = False

    def test(self, name: str) -> "SubtestSpy":
        self.called_with_name = name
        return self

    def __enter__(self) -> SubtestContextMock:
        self.context_yielded = True
        return SubtestContextMock()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        return False


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_verbose_mode_allocates_isolated_subtest_frame() -> None:
    """Verify that verbose=True routes execution through the subtests framework."""
    spy = SubtestSpy()
    checkpoint_name = "audit::critical_field"

    # Execute under verbose lane
    with maybe_subtest(spy, name=checkpoint_name, verbose=True) as ctx:
        assert isinstance(ctx, SubtestContextMock)
        # Inside the block, the execution must be actively managed
        assert spy.context_yielded is True

    # Verify that the native pytest subtest received the correct identifier
    assert spy.called_with_name == checkpoint_name


def test_silent_mode_bypasses_subtest_allocation_completely() -> None:
    """Verify that verbose=False behaves as a fast zero-overhead passthrough."""
    spy = SubtestSpy()

    # Execute under silent/fast lane
    with maybe_subtest(spy, name="ignored_checkpoint", verbose=False) as ctx:
        assert ctx is None
        # The subtest fixture must never be triggered
        assert spy.context_yielded is False
        assert spy.called_with_name is None