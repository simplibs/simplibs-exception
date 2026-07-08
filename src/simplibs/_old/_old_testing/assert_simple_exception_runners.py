from typing import Any, Callable


def test_function_is_callable(func):
    assert callable(func)

def test_valid_input(func, value):
    func(value)

def test_invalid_input(func, value, exception_type):
    try:
        func(value)
    except exception_type:
        return
    raise AssertionError(
        f"{exception_type.__name__} was not raised."
    )

def test_raise_function(func, exception_type):
    try:
        func()
    except exception_type:
        return
    raise AssertionError(
        f"{exception_type.__name__} was not raised."
    )

def run_tests(tests):
    for name, callback in tests:
        try:
            callback()
            print(f"{name} PASSED")
        except Exception:
            print(f"{name} FAILED")
            raise

from simplibs.sentinels import UNSET


def assert_simple_exception_runners(
    func,
    *,
    valid_value=UNSET,
    invalid_value=UNSET,
    exception_type=Exception,
):

    tests = [
        (
            "test_function_is_callable",
            lambda: test_function_is_callable(func),
        ),
    ]

    if valid_value is not UNSET:
        tests.append(
            (
                "test_valid_input",
                lambda: test_valid_input(
                    func,
                    valid_value,
                ),
            )
        )

    if invalid_value is not UNSET:
        tests.append(
            (
                "test_invalid_input",
                lambda: test_invalid_input(
                    func,
                    invalid_value,
                    exception_type,
                ),
            )
        )

    if valid_value is UNSET and invalid_value is UNSET:
        tests.append(
            (
                "test_raise_function",
                lambda: test_raise_function(
                    func,
                    exception_type,
                ),
            )
        )
    run_tests(tests)