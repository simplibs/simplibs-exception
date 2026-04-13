"""
Integration tests for SimpleException — full raise/catch flow, custom subclasses,
exception parameter, settings interaction, serialisation, oneline mode,
and tools (decorators/offsets) integration.
"""
import json
import pytest
from simplibs.exception.SimpleException import SimpleException
from simplibs.exception.core import SimpleExceptionSettings as S
from simplibs.exception.modes import LOG
from simplibs.exception.tools import raise_location_offset, raise_with_location_offset, bool_or_exception


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
# Exception parameter — isinstance flow
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
# Tools & Transformation Integration (Decorator, Offset, Context)
# -----------------------------------------------------------------------------

def test_raise_location_offset_integration():
    """Integration: decorator should shift location to the caller."""
    @raise_location_offset(offset=1)
    def my_utility_function():
        # Force get_location=True to trigger stack inspection
        raise SimpleException(problem="fail", get_location=True)

    with pytest.raises(SimpleException) as exc_info:
        my_utility_function()

    e = exc_info.value
    loc = e.caller_info

    # Verify that the reported function is not the internal utility function
    assert loc["function"] != "my_utility_function"

    # Verify that a valid location was captured
    assert "function" in loc


def test_exception_reraising_with_context_suppression():
    """Integration: verify that re-raising with offset suppresses original context."""
    try:
        raise ValueError("original cause")
    except ValueError as e:
        new_exc = SimpleException(exception=e, problem="wrapped")
        with pytest.raises(SimpleException) as exc_info:
            # Use utility to re-raise with offset
            raise_with_location_offset(new_exc, offset=1)

    # In test environments, __cause__ is None if 'from None' was used
    assert exc_info.value.__cause__ is None


def test_bool_or_exception_integration():
    """Integration: bool_or_exception must work as a shortcut for conditional exception raising."""
    assert bool_or_exception(return_bool=True, problem="an error") is False

    with pytest.raises(SimpleException) as exc_info:
        bool_or_exception(return_bool=False, problem="an error", error_name="BOOL_TEST")

    assert exc_info.value.error_name == "BOOL_TEST"
    assert exc_info.value.problem == "an error"


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
    # Explicitly enable location despite global settings (True defaults to depth 1)
    e = SimpleException(problem="an error", get_location=True)
    assert "File:" in str(e)


# -----------------------------------------------------------------------------
# Serialisation and Normalisation
# -----------------------------------------------------------------------------

def test_to_dict_reflects_actual_state():
    """to_dict must reflect the actual instance state after normalisation."""
    e = SimpleException(
        error_name="DICT_TEST",
        problem="an error",
        value=None,             # None is a valid set value
        how_to_fix=["A", "B"],  # List should be normalised to tuple
    )
    result = e.to_dict()
    assert result["error_name"] == "DICT_TEST"
    assert result["problem"] == "an error"
    assert result["value"] is None
    assert result["how_to_fix"] == ("A", "B")
    assert "message" not in result


def test_to_json_is_valid_and_consistent_with_to_dict():
    """to_json must be valid JSON consistent with to_dict."""
    e = SimpleException(error_name="JSON_TEST", problem="an error")
    data = json.loads(e.to_json())
    assert data["error_name"] == "JSON_TEST"
    assert data["problem"] == "an error"


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