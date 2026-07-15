from simplibs.exception.testing import assert_exception_function


from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_dynamic_cls_cache import (
    validate_dynamic_cls_cache,
)

from simplibs.exception.testing.__new.assert_exception_function import assert_exception_function
from simplibs.exception.testing.__new.assert_funkciton import (
    assert_exception_function_callable,
    assert_exception_function_raises,
    assert_exception_function_valid_input
)


def test_validate_dynamic_cls_cache(subtests):

    assert_exception_function(
        subtests,
        validate_dynamic_cls_cache,
        valid_params={},
        invalid_params="abc",
        exception_type=SimpleExceptionSettingsError,
        error_name="SETTINGS ERROR",
        label="_dynamic_cls_cache",
        expected="an empty dict {} — for configuration and state reset routines only",
        value="abc",
        problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
        how_to_fix=(
            "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
            "To clear this cache manually during hot-reloads or tests, assign an empty dict: "
            "SimpleExceptionSettings._dynamic_cls_cache = {}",
        ),
        verbose=True,
        intro=""
    )