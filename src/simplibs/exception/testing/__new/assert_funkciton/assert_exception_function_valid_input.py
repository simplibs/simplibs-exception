from typing import Any, Callable
from .._helpers import maybe_subtest, manage_param


def assert_exception_function_valid_input(
    subtests: Any,
    func: Callable[..., Any],
    *,
    valid_param: Any,
    verbose: bool = True,
    intro: str = "",
) -> None:
    """Assert that callable accepts valid input without raising."""

    args, kwargs = manage_param(valid_param)

    with maybe_subtest(
        subtests,
        name=f"{intro}test_valid_input",
        verbose=verbose,
    ):
        func(*args, **kwargs)