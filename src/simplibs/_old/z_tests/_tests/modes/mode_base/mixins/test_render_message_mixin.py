"""
Tests for RenderMessageMixin — scenario dispatching, validation trigger, and decoupled logic.
"""
import pytest
from simplibs.exception.core.SimpleExceptionData import SimpleExceptionData
from simplibs.exception.modes.mode_base.ModeBase import ModeBase
from simplibs.exception.core._internal_exceptions.SimpleExceptionModeError import SimpleExceptionModeError
from simplibs.sentinels import UNSET


# -----------------------------------------------------------------------------
# Test Implementations
# -----------------------------------------------------------------------------

class WorkflowTester(ModeBase):
    """
    Implementation dedicated to testing the logic within RenderMessageMixin.
    Signature matches the new protocol (only data is passed).
    """

    def _full_outcome(self, data: SimpleExceptionData) -> str:
        return "full"

    def _empty_outcome(self, data: SimpleExceptionData) -> str:
        return "empty"

    def _message_outcome(self, data: SimpleExceptionData) -> str:
        return "message"


@pytest.fixture
def tester():
    return WorkflowTester()


# -----------------------------------------------------------------------------
# Scenario Dispatching
# -----------------------------------------------------------------------------

def test_dispatch_empty_outcome(tester):
    """Should call _empty_outcome when no content fields and no message are provided."""
    data = SimpleExceptionData()  # All structured fields are UNSET
    assert tester.render_message(data, validate=False) == "empty"


def test_dispatch_message_outcome(tester):
    """Should call _message_outcome when only the message is set and structured fields are UNSET."""
    data = SimpleExceptionData(message="Something happened")
    assert tester.render_message(data, validate=False) == "message"


@pytest.mark.parametrize("field", ["value", "expected", "problem", "context", "how_to_fix"])
def test_dispatch_full_outcome(tester, field):
    """Should call _full_outcome if at least one structured content field is set."""
    val = "some data" if field != "how_to_fix" else ("fix step",)

    # Initialize with all UNSET except the one being tested
    data = SimpleExceptionData(**{field: val})
    assert tester.render_message(data, validate=False) == "full"


def test_full_outcome_priority_over_message(tester):
    """Full outcome must take priority if both message and structured fields are present."""
    data = SimpleExceptionData(message="Short message", problem="Detailed problem")
    assert tester.render_message(data, validate=False) == "full"


# -----------------------------------------------------------------------------
# Validation and Interface
# -----------------------------------------------------------------------------

def test_render_message_validation_trigger(tester):
    """Verify that validate=True triggers the lazy validation logic."""
    # Passing something that is not SimpleExceptionData should raise ModeError
    with pytest.raises(SimpleExceptionModeError):
        tester.render_message("not a data object", validate=True)


def test_is_callable_shortcut(tester):
    """The mode instance should be callable as a shortcut for render_message."""
    data = SimpleExceptionData(message="test")
    # This calls ModeBase.__call__ -> RenderMessageMixin.render_message
    assert tester(data, validate=False) == "message"


# -----------------------------------------------------------------------------
# Decoupling Verification
# -----------------------------------------------------------------------------

def test_render_message_does_not_handle_location_logic(tester):
    """
    Verify that render_message no longer interacts with location settings.
    It should simply pass the data object to the outcome methods.
    """
    data = SimpleExceptionData(problem="Decoupled test")
    data._get_location = 99  # Should be ignored by render_message logic

    # In the previous version, this would have triggered extract_caller_info.
    # Now it just dispatches based on content presence.
    assert tester.render_message(data, validate=False) == "full"