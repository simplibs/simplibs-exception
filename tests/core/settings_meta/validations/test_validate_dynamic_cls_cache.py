"""
Tests for SimpleExceptionSettingsError and validate_dynamic_cls_cache — inheritance, error name, and cache validation.
"""
import pytest
from simplibs.exception.core._internal_exceptions.SimpleExceptionInternalError import SimpleExceptionInternalError
from simplibs.exception.core._internal_exceptions.SimpleExceptionSettingsError import SimpleExceptionSettingsError
from simplibs.exception.core._settings_meta.validations.validate_dynamic_cls_cache import validate_dynamic_cls_cache


# -----------------------------------------------------------------------------
# SimpleExceptionSettingsError
# -----------------------------------------------------------------------------

def test_settings_error_inherits_from_internal_error():
    """SimpleExceptionSettingsError must inherit from SimpleExceptionInternalError."""
    assert isinstance(SimpleExceptionSettingsError(), SimpleExceptionInternalError)


def test_settings_error_default_error_name():
    """Default error_name must be 'SETTINGS ERROR'."""
    assert SimpleExceptionSettingsError().error_name == "SETTINGS ERROR"


# -----------------------------------------------------------------------------
# validate_dynamic_cls_cache
# -----------------------------------------------------------------------------

def test_empty_dict_passes():
    """An empty dict must pass — it is the only permitted cache reset value."""
    validate_dynamic_cls_cache({})


@pytest.mark.parametrize("value", [
    {"a": 1},
    None,
    "string",
    [],
    0,
])
def test_non_empty_value_raises(value):
    """Any value other than {} must raise SimpleExceptionSettingsError."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_dynamic_cls_cache(value)


def test_exception_contains_correct_fields():
    """The raised exception must have correctly populated fields."""
    invalid = {"a": 1}
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_dynamic_cls_cache(invalid)
    assert exc_info.value.value == invalid
    assert exc_info.value.value_label == "_dynamic_cls_cache"
    assert "an empty dict" in exc_info.value.expected
    assert exc_info.value.error_name == "SETTINGS ERROR"