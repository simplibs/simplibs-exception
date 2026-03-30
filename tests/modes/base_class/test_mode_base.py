"""
Tests for ModeBase — scenario dispatching, caller_info resolution, validation, and callable interface.
"""
import pytest
from unittest.mock import patch
from simplibs.exception.modes.base_class.ModeBase import ModeBase
from simplibs.exception.core.data.SimpleExceptionData import SimpleExceptionData
from simplibs.exception.modes.base_class._validations.SimpleExceptionModeError import SimpleExceptionModeError


# -----------------------------------------------------------------------------
# Test implementations
# -----------------------------------------------------------------------------

class ConcreteMode(ModeBase):
    """A concrete ModeBase implementation for testing purposes."""

    def _full_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        return "full"

    def _empty_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        return "empty"

    def _message_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        return "message"


class SpyMode(ModeBase):
    """A ModeBase implementation that captures the caller_info passed to the output method."""

    received_caller_info = None

    def _full_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        SpyMode.received_caller_info = caller_info
        return "full"

    def _empty_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        SpyMode.received_caller_info = caller_info
        return "empty"

    def _message_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        SpyMode.received_caller_info = caller_info
        return "message"


@pytest.fixture
def mode():
    return ConcreteMode()


@pytest.fixture
def spy_mode():
    SpyMode.received_caller_info = None
    return SpyMode()


# -----------------------------------------------------------------------------
# ABC — cannot be instantiated directly
# -----------------------------------------------------------------------------

def test_cannot_instantiate_mode_base_directly():
    """ModeBase is abstract — direct instantiation must raise TypeError."""
    with pytest.raises(TypeError):
        ModeBase()


# -----------------------------------------------------------------------------
# Scenario dispatching
# -----------------------------------------------------------------------------

def test_empty_outcome_when_no_data_and_no_message(mode):
    """Must call _empty_outcome when no content fields and no message are provided."""
    data = SimpleExceptionData()
    assert mode.render_message(data, validate=False) == "empty"


def test_message_outcome_when_only_message_is_set(mode):
    """Must call _message_outcome when only message is provided."""
    data = SimpleExceptionData(message="Something happened")
    assert mode.render_message(data, validate=False) == "message"


@pytest.mark.parametrize("attr", ["value", "expected", "problem", "context", "how_to_fix"])
def test_full_outcome_when_content_field_is_set(mode, attr):
    """Must call _full_outcome if at least one base content field is set."""
    kwargs = {attr: "some value" if attr != "how_to_fix" else ("fix it",)}
    data = SimpleExceptionData(**kwargs)
    assert mode.render_message(data, validate=False) == "full"


# -----------------------------------------------------------------------------
# caller_info
# -----------------------------------------------------------------------------

def test_caller_info_is_passed_to_outcome(spy_mode):
    """caller_info computed in render_message must be forwarded to the outcome method."""
    data = SimpleExceptionData()
    mock_info = {"file": "f.py", "line": 1, "full_path": "p/f.py", "function": "fn"}

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info", return_value=mock_info):
        spy_mode.render_message(data, validate=False)
        assert spy_mode.received_caller_info == mock_info


def test_caller_info_is_none_when_get_location_is_false(spy_mode):
    """caller_info must be None and extract_caller_info must not be called when _get_location=False."""
    data = SimpleExceptionData()
    data._get_location = False

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info") as mock_extract:
        spy_mode.render_message(data, validate=False)
        mock_extract.assert_not_called()
        assert spy_mode.received_caller_info is None


def test_extract_caller_info_called_with_correct_params(mode):
    """extract_caller_info must receive skip_frames=_get_location+1 and the correct excluded_patterns."""
    data = SimpleExceptionData()
    data._get_location = 2
    data._skip_locations = ("my_file.py",)

    with patch("simplibs.exception.modes.base_class.ModeBase.extract_caller_info") as mock_extract:
        mock_extract.return_value = None
        mode.render_message(data, validate=False)
        mock_extract.assert_called_once_with(
            skip_frames=3,
            excluded_patterns=("my_file.py",)
        )


# -----------------------------------------------------------------------------
# Validate
# -----------------------------------------------------------------------------

def test_validate_true_raises_for_invalid_data(mode):
    """validate=True must raise SimpleExceptionModeError for non-SimpleExceptionData input."""
    with pytest.raises(SimpleExceptionModeError):
        mode.render_message("not a data object", validate=True)


def test_validate_false_skips_validation(mode):
    """validate=False must not raise even for invalid data."""
    mode.render_message(SimpleExceptionData(), validate=False)


# -----------------------------------------------------------------------------
# __call__ and __repr__
# -----------------------------------------------------------------------------

def test_is_callable(mode):
    """The instance must be callable — delegates to render_message."""
    data = SimpleExceptionData()
    assert mode(data, validate=False) == "empty"


def test_repr(mode):
    """__repr__ must return the class name wrapped in mode format."""
    assert repr(mode) == "<ConcreteMode mode>"