import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_dynamic_cls_cache import (
    validate_dynamic_cls_cache,
)


def test_empty_dict_is_valid():
    """Confirms that an empty dictionary is permitted, enabling safe system state invalidation cycles."""
    assert validate_dynamic_cls_cache({}) is None


def test_non_empty_dict_raises():
    """Guarantees that attempting to overwrite the cache registry with populated data blocks triggers a settings error."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_dynamic_cls_cache({"key": "value"})


def test_non_dict_value_raises():
    """Ensures that passing completely foreign primitive types instantly trips the state machine guardrail."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_dynamic_cls_cache("not-a-dict")


def test_error_mentions_reset_method():
    """
    Verifies UX quality: the generated error payload must explicitly guide the engineer
    toward using the public 'reset()' API method for safe framework teardowns.
    """
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_dynamic_cls_cache("invalid")

    how_to_fix = exc_info.value.how_to_fix
    joined = how_to_fix if isinstance(how_to_fix, str) else " ".join(how_to_fix)

    assert "reset()" in joined


def test_error_payload_contains_precise_cache_diagnostic_metadata():
    """
    Architectural Contract: Verifies that the raised internal exception contains
    the exact structural metadata keys required for rendering the cache mutation failure.
    """
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_dynamic_cls_cache("corrupt-payload")

    err = exc_info.value

    # Assert strict layout definitions to guarantee intuitive terminal logs
    assert err.label == "_dynamic_cls_cache"
    assert "an empty dict {}" in err.expected
    assert "multi-inheritance class cache is handled internally" in err.problem