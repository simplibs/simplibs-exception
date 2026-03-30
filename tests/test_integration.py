"""
Integration tests for SimpleException — full raise/catch flow, custom subclasses, exception parameter,
settings interaction, serialisation, oneline mode, and bool_or_exception integration.
"""
import json
import pytest
from simplibs.exception.exception.SimpleException import SimpleException
from simplibs.exception.settings import SimpleExceptionSettings as S
from simplibs.exception.modes import LOG


@pytest.fixture(autouse=True)
def reset_settings():
    S.reset()
    yield
    S.reset()


# -----------------------------------------------------------------------------
# Core flow: create → raise → catch
# -----------------------------------------------------------------------------

def test_full_raise_catch_inspect():
    """Complete flow: raise → catch → inspect attributes."""
    with pytest.raises(SimpleException) as exc_info:
        raise SimpleException(
            error_name="INTEGRATION",
            problem="an error",
            value=42,
            value_label="parameter x",
            how_to_fix="Fix it",
        )

    e = exc_info.value
    assert e.error_name == "INTEGRATION"
    assert e.problem == "an error"
    assert e.value == 42
    assert e.value_label == "parameter x"
    assert e.how_to_fix == ("Fix it",)
    assert "INTEGRATION" in str(e)


def test_str_and_rendered_message_are_consistent():
    """str(e) and e._rendered_message must be identical."""
    e = SimpleException(problem="an error", get_location=False)
    assert str(e) == e._rendered_message


# -----------------------------------------------------------------------------
# Custom subclass with class-level attributes
# -----------------------------------------------------------------------------

def test_custom_subclass_uses_class_defaults():
    """A custom subclass with class-level attributes must work as a fully functional exception."""
    class ValidationError(SimpleException):
        error_name = "VALIDATION ERROR"
        expected = "a positive integer"
        how_to_fix = (
            "Provide a value greater than 0.",
            "Use the int type.",
        )

    with pytest.raises(ValidationError) as exc_info:
        raise ValidationError(value=-5, value_label="parameter age")

    e = exc_info.value
    assert e.error_name == "VALIDATION ERROR"
    assert e.expected == "a positive integer"
    assert e.value == -5
    assert isinstance(e, SimpleException)
    assert isinstance(e, ValidationError)


def test_custom_subclass_attribute_overridden_at_call():
    """A subclass class-level default must be overridable at the call site."""
    class MyError(SimpleException):
        error_name = "MY_ERROR"

    e = MyError(error_name="OVERRIDDEN")
    assert e.error_name == "OVERRIDDEN"


# -----------------------------------------------------------------------------
# exception parameter — isinstance flow
# -----------------------------------------------------------------------------

def test_exception_class_enables_isinstance():
    """exception=ValueError must make isinstance(e, ValueError) return True."""
    with pytest.raises(SimpleException) as exc_info:
        raise SimpleException(exception=ValueError, problem="negative value")

    e = exc_info.value
    assert isinstance(e, ValueError)
    assert isinstance(e, SimpleException)


def test_exception_instance_from_except_block():
    """Passing an instance from an except block must store both the type and the message."""
    try:
        raise ValueError("original error")
    except ValueError as original:
        e = SimpleException(exception=original, problem="caught error")

    assert isinstance(e, ValueError)
    assert e._intercepted_exception == "original error"
    assert "original error" in str(e)


def test_exception_cached_class_is_reused():
    """The same (class, exception) combination must reuse the cached dynamic class."""
    e1 = SimpleException(exception=ValueError, problem="first")
    e2 = SimpleException(exception=ValueError, problem="second")
    assert type(e1) is type(e2)


# -----------------------------------------------------------------------------
# Settings affect output
# -----------------------------------------------------------------------------

def test_settings_mode_change_affects_output():
    """Changing DEFAULT_MESSAGE_MODE must affect the output of all subsequent exceptions."""
    S.DEFAULT_MESSAGE_MODE = LOG
    e = SimpleException(problem="an error", get_location=False)
    assert "error=" in str(e)
    assert "═" not in str(e)


def test_settings_get_location_false_disables_location():
    """DEFAULT_GET_LOCATION=False must disable location reporting globally."""
    S.DEFAULT_GET_LOCATION = False
    e = SimpleException(problem="an error")
    assert "File:" not in str(e)


def test_instance_get_location_overrides_settings():
    """The get_location parameter at the call site must take precedence over settings."""
    S.DEFAULT_GET_LOCATION = False
    e = SimpleException(problem="an error", get_location=False)
    assert "File:" not in str(e)


# -----------------------------------------------------------------------------
# Serialisation in real use
# -----------------------------------------------------------------------------

def test_to_dict_reflects_actual_state():
    """to_dict must reflect the actual instance state after normalisation."""
    e = SimpleException(
        error_name="DICT_TEST",
        problem="an error",
        value=None,           # None is not UNSET — must be included
        how_to_fix=["A", "B"],  # list → normalised to tuple
    )
    result = e.to_dict()
    assert result["error_name"] == "DICT_TEST"
    assert result["problem"] == "an error"
    assert result["value"] is None
    assert result["how_to_fix"] == ("A", "B")
    assert "message" not in result


def test_to_debug_dict_contains_computed_values():
    """to_debug_dict must contain both input data and computed values."""
    e = SimpleException(problem="an error", get_location=False)
    result = e.to_debug_dict()
    assert "problem" in result              # public attribute
    assert "_get_location" in result        # private annotated
    assert "_rendered_message" in result    # private unannotated


def test_to_json_is_valid_and_consistent_with_to_dict():
    """to_json must be valid JSON consistent with to_dict."""
    e = SimpleException(error_name="JSON_TEST", problem="an error")
    data = json.loads(e.to_json())
    assert data == {k: v for k, v in e.to_dict().items() if not callable(v)}


# -----------------------------------------------------------------------------
# Oneline mode
# -----------------------------------------------------------------------------

def test_oneline_param_produces_single_line():
    """oneline=True must produce a single-line output regardless of content."""
    e = SimpleException(
        error_name="ONELINE_TEST",
        problem="an error",
        expected="str",
        value=42,
        how_to_fix=("Fix it",),
        oneline=True,
    )
    assert "\n" not in str(e).strip()


# -----------------------------------------------------------------------------
# bool_or_exception integration
# -----------------------------------------------------------------------------

def test_bool_or_exception_integration():
    """bool_or_exception must work as a shortcut for conditional exception raising."""
    from simplibs.exception.utils import bool_or_exception

    assert bool_or_exception(return_bool=True, problem="an error") is False

    with pytest.raises(SimpleException) as exc_info:
        bool_or_exception(return_bool=False, problem="an error", error_name="BOOL_TEST")

    assert exc_info.value.error_name == "BOOL_TEST"
    assert exc_info.value.problem == "an error"