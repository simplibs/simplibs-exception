from typing import Any, Callable

import pytest
from simplibs.sentinels import UNSET


def assert_simple_exception_subtest(
    subtests,
    func: Callable[..., Any],
    *,
    valid_value: Any = UNSET,
    invalid_value: Any = UNSET,
    exception_type: type[BaseException] = Exception,
):

    with subtests.test("test_function_is_callable"):
        assert callable(func)

    if valid_value is not UNSET:
        with subtests.test("test_valid_input"):
            func(valid_value)

    if invalid_value is not UNSET:
        with subtests.test("test_invalid_input"):
            with pytest.raises(exception_type):
                func(invalid_value)

    if valid_value is UNSET and invalid_value is UNSET:
        with subtests.test("test_raise_function"):
            with pytest.raises(exception_type):
                func()
