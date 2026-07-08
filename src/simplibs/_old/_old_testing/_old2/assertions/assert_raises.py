from typing import Any, Callable
# Outers
from ..call_repr import describe_call
# Inners
from .assert_exception_fields import assert_exception_fields


def assert_raises(
    func: Callable[..., Any],
    *args: Any,
    exception_type: type[BaseException] = Exception,
    expected: dict[str, Any] | None = None,
    **kwargs: Any,
) -> BaseException:
    """
    Calls `func(*args, **kwargs)` and asserts that it raises an exception
    of type `exception_type`. Optionally also verifies selected attributes
    on the caught exception via `expected`.

    Framework-agnostic: uses plain try/except + assert, so it works the
    same whether called from pytest, unittest, or a plain script.

    Args:
        func: The callable expected to raise.
        *args: Positional arguments passed to `func`.
        exception_type: The exception type expected to be raised.
        expected: Optional mapping of {attribute_name: expected_value} to
                  verify on the caught exception (see assert_exception_fields).
        **kwargs: Keyword arguments passed to `func`.

    Returns:
        The caught exception instance, for any further manual inspection.

    Raises:
        AssertionError: If `func` does not raise, raises the wrong
                        exception type, or fails the `expected` field check.
    """

    # 1. Zkouška za funkce vyvolá výjimku
    try:
        func(*args, **kwargs)

    # 2. Vyřízení když zda vyvolaný výjimka odpovídá očekávané
    except exception_type as exc:
        if expected:
            assert_exception_fields(exc, expected)
        return exc

    # 3. Vyřízení pokud výjimka neodpovídá očekávané
    except BaseException as unexpected:
        raise AssertionError(
            f"{describe_call(func, args, kwargs)} raised "
            f"{type(unexpected).__name__} instead of the expected "
            f"{exception_type.__name__}."
        ) from unexpected

    # 4. Vyřízení když funkce nevyvolala výjimku
    raise AssertionError(
        f"{describe_call(func, args, kwargs)} did not raise "
        f"{exception_type.__name__} as expected."
    )