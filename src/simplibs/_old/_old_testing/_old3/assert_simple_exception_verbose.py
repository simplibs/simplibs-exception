import pytest
from typing import Any, Callable
from simplibs.sentinels import UNSET, UnsetType
from ..SimpleException import SimpleException, SimpleExceptionData


def manage_param(param):
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}

    if isinstance(param, dict):
        if param:
            kwargs = param
        else:
            args = (param,)
    elif isinstance(param, (tuple, list)):
        if param:
            args = tuple(param)
        else:
            args = (param,)
    else:
        args = (param,)

    return args, kwargs


def compare_strings(test_value, exc_value, exact_match):
    if exact_match:
        assert test_value == exc_value
    else:
        if isinstance(test_value, tuple):
            test_value = " ".join(test_value)
        if isinstance(exc_value, tuple):
            exc_value = " ".join(exc_value)
        assert test_value in exc_value


class maybe_subtest:
    def __init__(self, subtests, name, verbose):
        self.subtests = subtests
        self.name = name
        self.verbose = verbose
        self.ctx = None

    def __enter__(self):
        if self.verbose:
            self.ctx = self.subtests.test(self.name)
            return self.ctx.__enter__()
        return None

    def __exit__(self, exc_type, exc, tb):
        if self.verbose:
            return self.ctx.__exit__(exc_type, exc, tb)
        return False


def assert_simple_exception_verbose(
    subtests,
    func: Callable[..., Any],
    *,
    valid_param: Any = UNSET,
    invalid_param: Any = UNSET,
    exception_type: type[BaseException] = SimpleException,

    error_name: str | UnsetType = UNSET,
    label: str | None | UnsetType = UNSET,
    message: str | None | UnsetType = UNSET,
    expected: str | None | UnsetType = UNSET,
    value: Any = UNSET,
    problem: "str | tuple[str, ...] | None | UnsetType" = UNSET,
    context: "str | tuple[str, ...] | None | UnsetType" = UNSET,
    how_to_fix: "str | tuple[str, ...] | None | UnsetType" = UNSET,
    exception: "Exception | type[Exception] | None | UnsetType" = UNSET,
    get_location: "bool | int | UnsetType" = UNSET,
    skip_locations: "tuple[str, ...] | UnsetType" = UNSET,
    oneline: "bool | UnsetType" = UNSET,

    exact_match: bool = True,
    verbose: bool = True,
) -> BaseException | None:



    # 1. Funkce je callable
    with maybe_subtest(subtests, "test_function_is_callable", verbose):
        assert callable(func)

    # 2. Validní parametry
    if valid_param is not UNSET:
        args, kwargs = manage_param(valid_param)
        with maybe_subtest(subtests, "test_valid_input", verbose):
            func(*args, **kwargs)

    # 3. Vyvolání výjimky
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}

    if invalid_param is not UNSET:
        args, kwargs = manage_param(invalid_param)

    with maybe_subtest(subtests, "test_function_raise_exception", verbose):
        with pytest.raises(exception_type) as exc_info:
            func(*args, **kwargs)

    exc = exc_info.value

    # 5. error_name
    if error_name is not UNSET:
        with maybe_subtest(subtests, "test_error_name", verbose):
            compare_strings(error_name, exc.error_name, exact_match)

    # 6. label
    if label is not UNSET:
        with maybe_subtest(subtests, "test_label", verbose):
            compare_strings(label, exc.label, exact_match)

    # 7. message
    if message is not UNSET:
        with maybe_subtest(subtests, "test_message", verbose):
            compare_strings(message, exc.message, exact_match)

    # 8. expected
    if expected is not UNSET:
        with maybe_subtest(subtests, "test_expected", verbose):
            compare_strings(expected, exc.expected, exact_match)

    # 9. value
    if value is not UNSET:
        with maybe_subtest(subtests, "test_value", verbose):
            assert value == exc.value

    # 10. problem
    if problem is not UNSET:
        with maybe_subtest(subtests, "test_problem", verbose):
            compare_strings(problem, exc.problem, exact_match)

    # 11. context
    if context is not UNSET:
        with maybe_subtest(subtests, "test_context", verbose):
            compare_strings(context, exc.context, exact_match)

    # 12. how_to_fix
    if how_to_fix is not UNSET:
        with maybe_subtest(subtests, "test_how_to_fix", verbose):
            compare_strings(how_to_fix, exc.how_to_fix, exact_match)

    # 13. exception
    if exception is not UNSET:
        with maybe_subtest(subtests, "test_exception", verbose):
            assert exception == exc.exception

    # 14. get_location
    if get_location is not UNSET:
        with maybe_subtest(subtests, "test_get_location", verbose):
            assert get_location == exc.get_location

    # 15. skip_locations
    if skip_locations is not UNSET:
        with maybe_subtest(subtests, "test_skip_locations", verbose):
            assert skip_locations == exc.skip_locations

    # 16. oneline
    if oneline is not UNSET:
        with maybe_subtest(subtests, "test_oneline", verbose):
            assert oneline == exc.oneline

    return exc