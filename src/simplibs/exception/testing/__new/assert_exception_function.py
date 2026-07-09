from typing import Any, Callable
from simplibs.sentinels import UnsetType, UNSET

from .assert_funkciton import (
    assert_exception_function_valid_input,
    assert_exception_function_raises,
    assert_exception_function_callable
)
from .assert_fields import assert_exception_fields
from ._helpers import maybe_subtest


def assert_exception_function(
    subtests: Any,
    func: Callable[..., Any],
    *,
    valid_param: Any = UNSET,
    invalid_param: Any = UNSET,
    exception_type: type[BaseException],
    error_name: str | UnsetType = UNSET,
    label: str | None | UnsetType = UNSET,
    message: str | None | UnsetType = UNSET,
    expected: str | None | UnsetType = UNSET,
    value: Any = UNSET,
    problem: str | tuple[str, ...] | None | UnsetType = UNSET,
    context: str | tuple[str, ...] | None | UnsetType = UNSET,
    how_to_fix: str | tuple[str, ...] | None | UnsetType = UNSET,
    exception: Exception | type[Exception] | None | UnsetType = UNSET,
    get_location: bool | int | UnsetType = UNSET,
    skip_locations: tuple[str, ...] | UnsetType = UNSET,
    oneline: bool | UnsetType = UNSET,

    exact_match: bool = True,
    verbose: bool = True,
    intro:str = "",
    deep_check: bool = True
) -> BaseException:

    assert_exception_function_callable(
        subtests,
        func,

        verbose=verbose,
        intro=intro
    )

    exc = assert_exception_function_raises(
        subtests,
        func,

        invalid_param=invalid_param,
        exception_type=exception_type,

        verbose=verbose,
        intro=intro
    )

    if deep_check:

        if valid_param is not UNSET:
            assert_exception_function_valid_input(
                subtests,
                func,

                valid_param=valid_param,

                verbose=verbose,
                intro=intro
            )

        assert_exception_fields(
            subtests,
            exc,

            error_name=error_name,
            label=label,
            message=message,
            expected=expected,
            value=value,
            problem=problem,
            context=context,
            how_to_fix=how_to_fix,
            exception=exception,
            get_location=get_location,
            skip_locations=skip_locations,
            oneline=oneline,

            exact_match=exact_match,
            verbose=verbose,
            intro=intro
        )

    return exc
