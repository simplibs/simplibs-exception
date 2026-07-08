"""
Tests for NormalizeParamMixin — value preservation, fallback to class defaults, and inheritance.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.core._exception_mixins.normalizers.NormalizeParam import NormalizeParamMixin


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockData(NormalizeParamMixin):
    error_name = "DEFAULT_ERROR"
    message = "Default message"
    is_active = True


@pytest.fixture
def normalizer():
    return MockData()


# -----------------------------------------------------------------------------
# Valid values — preservation
# -----------------------------------------------------------------------------

def test_correct_type_is_preserved(normalizer):
    """A value of the correct type must be returned unchanged."""
    assert normalizer._normalize_param("MY_ERR", "error_name", str) == "MY_ERR"


def test_false_bool_is_preserved(normalizer):
    """False must be preserved — it must not be treated as a falsy fallback trigger."""
    assert normalizer._normalize_param(False, "is_active", bool) is False


# -----------------------------------------------------------------------------
# Fallback to class-level default
# -----------------------------------------------------------------------------

def test_wrong_type_falls_back_to_class_default(normalizer):
    """A value of the wrong type must be replaced by the class-level default."""
    assert normalizer._normalize_param(123, "error_name", str) == "DEFAULT_ERROR"


def test_none_falls_back_to_class_default(normalizer):
    """None must trigger the fallback if None is not the expected type."""
    assert normalizer._normalize_param(None, "message", str) == "Default message"


def test_unset_falls_back_to_class_default(normalizer):
    """UNSET must trigger the fallback — it is the most common real-world input."""
    assert normalizer._normalize_param(UNSET, "error_name", str) == "DEFAULT_ERROR"


# -----------------------------------------------------------------------------
# Inheritance
# -----------------------------------------------------------------------------

def test_subclass_default_has_priority():
    """The fallback must come from the concrete class, not from the parent."""
    class CustomData(MockData):
        error_name = "CUSTOM_DEFAULT"

    obj = CustomData()
    assert obj._normalize_param(42, "error_name", str) == "CUSTOM_DEFAULT"


# -----------------------------------------------------------------------------
# Custom types
# -----------------------------------------------------------------------------

def test_custom_class_instance_is_preserved(normalizer):
    """A valid instance of a custom class must be returned unchanged."""
    class Dummy:
        pass

    d = Dummy()
    assert normalizer._normalize_param(d, "message", Dummy) is d


def test_wrong_custom_class_falls_back(normalizer):
    """An instance of the wrong class must trigger the fallback."""
    class Dummy:
        pass

    assert normalizer._normalize_param("not a dummy", "message", Dummy) == "Default message"