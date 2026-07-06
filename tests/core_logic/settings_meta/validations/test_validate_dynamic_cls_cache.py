import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_dynamic_cls_cache import (
    validate_dynamic_cls_cache,
)


def test_empty_dict_is_valid():
    # Must not raise.
    assert validate_dynamic_cls_cache({}) is None


def test_non_empty_dict_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_dynamic_cls_cache({"key": "value"})


def test_non_dict_value_raises():
    with pytest.raises(SimpleExceptionSettingsError):
        validate_dynamic_cls_cache("not-a-dict")


def test_error_mentions_reset_method():
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_dynamic_cls_cache("invalid")

    how_to_fix = exc_info.value.how_to_fix
    joined = how_to_fix if isinstance(how_to_fix, str) else " ".join(how_to_fix)
    assert "reset()" in joined
