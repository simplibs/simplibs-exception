import pytest

from simplibs.exception._core_logic.internal_exceptions import (
    SimpleExceptionInternalError,
    SimpleExceptionModeError,
    SimpleExceptionSettingsError
)

from simplibs.exception._core_logic.settings_meta.validations import (
    raise_unknown_settings_attribute_error,
    raise_system_blacklist_mutation_error,
    validate_dynamic_cls_cache,
    validate_get_location,
    validate_location_blacklist,
    validate_message_mode,
    validate_value_truncation_length
)

from simplibs.exception.testing.generate_bulk_tests import generate_bulk_tests
from simplibs.exception.testing.auxiliary_classes.TestCase import TestCase

class DummyClass:
    _VALIDATORS = {
        "GET_LOCATION": validate_get_location,
        "LOCATION_BLACKLIST": validate_location_blacklist,
        "MESSAGE_MODE": validate_message_mode,
        "VALUE_TRUNCATION_LENGTH": validate_value_truncation_length,
        "_dynamic_cls_cache": validate_dynamic_cls_cache,
    }


VALIDATE_DYNAMIC_CLS_CACHE_CASE = TestCase(
    func=validate_dynamic_cls_cache,

    valid_param={},
    invalid_param="abc",

    exception_type=SimpleExceptionSettingsError,

    error_name="SETTINGS ERROR",
    label="_dynamic_cls_cache",
    expected="an empty dict {} — for configuration and state reset routines only",
    value="abc",

    problem=(
        "the multi-inheritance class cache is handled internally "
        "and cannot be manually overwritten"
    ),

    how_to_fix=(
        "To wipe the framework runtime state safely, invoke: "
        "SimpleExceptionSettings.reset()",

        "To clear this cache manually during hot-reloads or tests, "
        "assign an empty dict: "
        "SimpleExceptionSettings._dynamic_cls_cache = {}",
    ),
)

ITEMS = [
    # 1) Definiční třídy výjimek
    SimpleExceptionInternalError,
    SimpleExceptionModeError,
    SimpleExceptionSettingsError,

    # 3) Kompletní testovací scénáře
    VALIDATE_DYNAMIC_CLS_CACHE_CASE,

    # 2) Raise funkce bez parametrů
    (SimpleExceptionSettingsError, raise_unknown_settings_attribute_error, DummyClass, "name"),
    (SimpleExceptionSettingsError, raise_system_blacklist_mutation_error, "value"),

    # 3) Validační funkce s parametry
    (SimpleExceptionSettingsError, validate_dynamic_cls_cache, "invalide_umput"),
    (SimpleExceptionSettingsError, validate_get_location, "invalide_umput"),
    (SimpleExceptionSettingsError, validate_location_blacklist, "invalide_umput"),
    (SimpleExceptionSettingsError, validate_location_blacklist, (1,)),
    (SimpleExceptionSettingsError, validate_message_mode, "invalide_umput"),
    (SimpleExceptionSettingsError, validate_value_truncation_length, "invalide_umput"),
    (SimpleExceptionSettingsError, validate_value_truncation_length, -1),
]

def test_bulk(subtests):
    generate_bulk_tests(subtests, ITEMS, verbose=True, deep_check=False)