"""
Tests for maybe_subtest — conditional proxy isolation, execution modes, and context delegation.
"""
import pytest
from simplibs.exception.testing._helpers.common.maybe_subtest import maybe_subtest


# -----------------------------------------------------------------------------
# Test Doubles & Mocks
# -----------------------------------------------------------------------------

class SubtestContextMock:
    """Mock representing the active context manager returned by pytest-subtests."""
    def __init__(self):
        self.entered = False
        self.exited = False

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exited = True
        # Return True to simulate exception suppression if an error occurred, 
        # or False under normal conditions. We'll return False for standard pass.
        return False


class SubtestEngineSpy:
    """Spy to track if the subtest registry is triggered and monitor lifecycle execution."""
    def __init__(self):
        self.recorded_name = None
        self.context_mock = SubtestContextMock()

    def test(self, name):
        """Implements the required subtests.test(name) boundary factory."""
        self.recorded_name = name
        return self.context_mock


# -----------------------------------------------------------------------------
# Bi-Modal Operational Matrix Tests
# -----------------------------------------------------------------------------

def test_verbose_mode_activates_and_delegates_subtest():
    """Under verbose=True, the proxy must register the subtest and delegate the full lifecycle."""
    spy = SubtestEngineSpy()
    test_name = "isolated_checkpoint"

    with maybe_subtest(spy, name=test_name, verbose=True) as ctx:
        # Verify the subtest was requested with the correct diagnostic name
        assert spy.recorded_name == test_name
        # Verify __enter__ was forwarded and executed on the underlying context
        assert spy.context_mock.entered is True
        assert ctx is spy.context_mock

    # Verify __exit__ was successfully forwarded and executed upon leaving the block
    assert spy.context_mock.exited is True


def test_silent_mode_is_a_pure_passthrough():
    """Under verbose=False, the engine must execute as a no-op passthrough with zero allocation."""
    spy = SubtestEngineSpy()

    with maybe_subtest(spy, name="silent_checkpoint", verbose=False) as ctx:
        # The inner block must still execute, but the proxy should bypass the subtest engine completely
        assert ctx is None
        assert spy.recorded_name is None
        assert spy.context_mock.entered is False

    assert spy.context_mock.exited is False


# -----------------------------------------------------------------------------
# Error Propagation & Boundary Exception Handling
# -----------------------------------------------------------------------------

def test_exceptions_bubble_up_normally():
    """Verify that exceptions raised inside the context block are not swallowed blindly."""
    spy = SubtestEngineSpy()

    with pytest.raises(ValueError, match="trigger"):
        with maybe_subtest(spy, name="error_checkpoint", verbose=True):
            raise ValueError("trigger")

    # Ensure even during a crash, the underlying exit lifecycle was closed
    assert spy.context_mock.exited is True