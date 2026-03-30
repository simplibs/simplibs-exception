"""
Tests for SimpleException — instantiation, parameter normalisation, subclassing, output modes, and serialisation.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.exception.SimpleException import SimpleException
from simplibs.exception.core import SimpleExceptionInternalError
from simplibs.exception.settings import SimpleExceptionSettings as S


@pytest.fixture(autouse=True)
def reset_settings():
    S.reset()
    yield
    S.reset()


# -----------------------------------------------------------------------------
# Basic instantiation
# -----------------------------------------------------------------------------

def test_can_be_instantiated_without_arguments():
    """SimpleException must be instantiable without any arguments."""
    e = SimpleException()
    assert isinstance(e, SimpleException)
    assert isinstance(e, Exception)


def test_can_be_raised_and_caught():
    """SimpleException must be raiseable and catchable as a standard exception."""
    with pytest.raises(SimpleException):
        raise SimpleException(problem="something went wrong")


# -----------------------------------------------------------------------------
# __init__ — parameter normalisation
# -----------------------------------------------------------------------------

def test_valid_params_are_stored():
    """Valid parameters must be stored as instance attributes."""
    e = SimpleException(
        message="a message",
        value=42,
        value_label="parameter",
        expected="str",
        problem="wrong type",
        context="inside a loop",
        error_name="MY_ERROR",
    )
    assert e.message == "a message"
    assert e.value == 42
    assert e.value_label == "parameter"
    assert e.expected == "str"
    assert e.problem == "wrong type"
    assert e.context == "inside a loop"
    assert e.error_name == "MY_ERROR"


def test_invalid_param_type_falls_back_to_class_default():
    """A parameter of the wrong type must be replaced by the class-level default."""
    e = SimpleException(error_name=123)
    assert e.error_name == "ERROR"


def test_how_to_fix_string_is_normalized_to_tuple():
    """how_to_fix passed as a string must be normalised to a tuple."""
    e = SimpleException(how_to_fix="Fix it", problem="error")
    assert e.how_to_fix == ("Fix it",)


def test_unset_params_remain_unset():
    """Parameters that were not provided must remain UNSET."""
    e = SimpleException()
    assert e.message is UNSET
    assert e.value is UNSET
    assert e.expected is UNSET


# -----------------------------------------------------------------------------
# exception parameter
# -----------------------------------------------------------------------------

def test_exception_class_makes_instance_isinstance():
    """After passing exception=ValueError, the instance must be isinstance(e, ValueError)."""
    e = SimpleException(exception=ValueError, problem="error")
    assert isinstance(e, ValueError)


def test_exception_instance_is_processed():
    """Passing an exception instance must store the type and the message."""
    original = RuntimeError("original message")
    e = SimpleException(exception=original, problem="error")
    assert isinstance(e, RuntimeError)
    assert e._intercepted_exception == "original message"


# -----------------------------------------------------------------------------
# Class-level attributes on subclasses
# -----------------------------------------------------------------------------

def test_subclass_class_attributes_are_used_as_defaults():
    """Class-level attributes defined on a subclass must be used as defaults."""
    class MyError(SimpleException):
        error_name = "MY_ERROR"
        expected = "a positive integer"

    e = MyError(value=42)
    assert e.error_name == "MY_ERROR"
    assert e.expected == "a positive integer"


def test_subclass_attribute_can_be_overridden_at_call():
    """A subclass class-level default must be overridable at the call site."""
    class MyError(SimpleException):
        error_name = "MY_ERROR"

    e = MyError(error_name="OVERRIDE")
    assert e.error_name == "OVERRIDE"


def test_invalid_subclass_attribute_raises_at_definition():
    """A typo in a subclass attribute must raise an error at class definition time."""
    with pytest.raises(SimpleExceptionInternalError):
        class BadError(SimpleException):
            errro_name = "TYPO"


# -----------------------------------------------------------------------------
# _render_message and output modes
# -----------------------------------------------------------------------------

def test_str_returns_rendered_message():
    """str(e) must return the assembled message string."""
    e = SimpleException(problem="error")
    assert str(e) == e._rendered_message
    assert len(str(e)) > 0


def test_oneline_mode_is_single_line():
    """oneline=True must produce a single-line output."""
    e = SimpleException(problem="error", oneline=True)
    assert "\n" not in str(e).strip()


def test_default_mode_is_pretty():
    """The default mode must be PRETTY — the output must contain the double line."""
    from simplibs.exception.modes.PRETTY import PRETTY as pretty_instance
    e = SimpleException(problem="error", get_location=False)
    assert pretty_instance.double_line in str(e)


def test_custom_mode_via_settings_is_used():
    """Changing DEFAULT_MESSAGE_MODE in settings must affect the output."""
    from simplibs.exception.modes import ONELINE as oneline_instance
    S.DEFAULT_MESSAGE_MODE = oneline_instance
    e = SimpleException(problem="error", get_location=False)
    assert "\n" not in str(e).strip()


# -----------------------------------------------------------------------------
# __repr__ and __str__
# -----------------------------------------------------------------------------

def test_repr_format():
    """__repr__ must return a correctly formatted string."""
    e = SimpleException(error_name="TEST", value=42)
    assert repr(e) == "<SimpleException(error_name='TEST', value=42)>"


def test_repr_subclass_uses_subclass_name():
    """__repr__ on a subclass must use the subclass name."""
    class MyError(SimpleException):
        pass

    e = MyError()
    assert repr(e).startswith("<MyError(")


# -----------------------------------------------------------------------------
# Serialisation
# -----------------------------------------------------------------------------

def test_to_dict_contains_set_public_attributes():
    """to_dict must contain all set public attributes."""
    e = SimpleException(error_name="DICT_TEST", problem="error")
    result = e.to_dict()
    assert result["error_name"] == "DICT_TEST"
    assert result["problem"] == "error"
    assert "message" not in result


def test_to_debug_dict_contains_private_attributes():
    """to_debug_dict must contain private attributes — both annotated and unannotated."""
    e = SimpleException(problem="error", get_location=False)
    result = e.to_debug_dict()
    # Annotated private attributes (from SimpleExceptionData)
    assert "_get_location" in result
    assert "_oneline" in result
    assert "_skip_locations" in result
    # Unannotated private attributes (assigned in __init__)
    assert "_rendered_message" in result


def test_to_json_returns_valid_json():
    """to_json must return a valid JSON string."""
    import json
    e = SimpleException(error_name="JSON_TEST", problem="error")
    data = json.loads(e.to_json())
    assert data["error_name"] == "JSON_TEST"