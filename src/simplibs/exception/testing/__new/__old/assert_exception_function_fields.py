from typing import Any, Callable
from simplibs.sentinels import UnsetType, UNSET
from ..assert_fields import assert_exception_fields
from .._helpers import manage_param, maybe_subtest
import pytest

def assert_exception_function_fields(
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
    intro=""
) -> Any:
    """Assert captured exception telemetry fields."""

    args, kwargs = manage_param(invalid_param)

    with maybe_subtest(
        subtests,
        name=f"{intro}test_raises_exception",
        verbose=verbose,
    ):
        with pytest.raises(BaseException) as exc_info:
            func(*args, **kwargs)

    exc = exc_info.value

    # 3. Forward the caught exception instance to the properties validator
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
    )

    return exc
