from typing import Any, Callable
# Outers
from ..call_repr import describe_call


def assert_does_not_raise(
    func: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    Calls `func(*args, **kwargs)` and asserts that it does NOT raise.

    Args:
        func: The callable expected to succeed.
        *args: Positional arguments passed to `func`.
        **kwargs: Keyword arguments passed to `func`.

    Returns:
        Whatever `func` returns (typically None for validate_ functions,
        kept generic for any future use case).

    Raises:
        AssertionError: If `func` raises any exception.
    """

    # 1. Zkouška zda funkce nevyvolá výjimku
    try:
        return func(*args, **kwargs)

    # 2. Vyřízení pokud výjimky byla vyvolaná
    except Exception as unexpected:
        raise AssertionError(
            f"{describe_call(func, args, kwargs)} was expected to pass "
            f"without raising, but raised {type(unexpected).__name__}: "
            f"{unexpected}"
        ) from unexpected