from typing import Any, Callable
from simplibs.sentinels import UnsetType, UNSET
from .._helpers import maybe_subtest, manage_param
import pytest

def assert_exception_function_raises(
    subtests: Any,
    func: Callable[..., Any],
    *,
    invalid_param: Any,
    exception_type: (
        type[BaseException]
        | tuple[type[BaseException], ...]
        | UnsetType
    ) = UNSET,
    verbose: bool = True,
    intro: str = "",
) -> BaseException:

    args, kwargs = manage_param(invalid_param)

    with maybe_subtest(
        subtests,
        name=f"{intro}test_raises_exception",
        verbose=verbose,
    ):
        with pytest.raises(BaseException) as exc_info:
            func(*args, **kwargs)

    exc = exc_info.value

    if exception_type is not UNSET:
        with maybe_subtest(
            subtests,
            name=f"{intro}test_exception_type",
            verbose=verbose,
        ):
            # noinspection PyTypeChecker
            assert isinstance(exc, exception_type)

    return exc