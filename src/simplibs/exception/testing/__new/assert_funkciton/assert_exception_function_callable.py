from typing import Any, Callable
from .._helpers import maybe_subtest


def assert_exception_function_callable(
    subtests: Any,
    func: Callable[..., Any],
    *,
    verbose: bool = True,
    intro: str = "",
) -> Callable[..., Any]:
    """Assert that target object is callable."""

    with maybe_subtest(
        subtests,
        name=f"{intro}test_callable",
        verbose=verbose,
    ):
        assert callable(func)

    return func