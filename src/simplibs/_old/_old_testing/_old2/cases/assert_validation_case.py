from typing import Any, Callable
# Outers
from ..assertions import assert_does_not_raise, assert_raises


def assert_validation_case(
    func: Callable[..., Any],
    *,
    valid: tuple[tuple[Any, ...], dict[str, Any]] | None = None,
    invalid: tuple[tuple[Any, ...], dict[str, Any]] | None = None,
    exception_type: type[BaseException] = Exception,
    expected: dict[str, Any] | None = None,
) -> BaseException | None:
    """
    Generic, framework-agnostic test-case for a validate_/raise_ function
    pair. Not tied to SimpleException's specific field set — this is the
    general-purpose escape hatch for any callable, including ones taking
    more than one positional argument (e.g. `check_children_attributes`),
    for which the SimpleException-tailored `assert_simple_exception` isn't
    a good fit.

    Args:
        func: The function under test (a validate_... or raise_... function).
        valid: (args, kwargs) for an input that must NOT raise. Omit to
               skip the positive check.
        invalid: (args, kwargs) for an input that must raise. Omit to skip
                 the negative check.
        exception_type: Expected exception type for the `invalid` case.
        expected: Expected attributes on the caught exception (see
                  assert_exception_fields). Only used if `invalid` is given.

    Returns:
        The caught exception from the `invalid` case, or None if `invalid`
        was not provided.

    Raises:
        AssertionError: If either check fails.
    """

    # 1. Kontrola pro validní hodnotu (výjimka se nemá nevyvolat)
    if valid is not None:
        valid_args, valid_kwargs = valid
        assert_does_not_raise(func, *valid_args, **valid_kwargs)

    # 2. Kontrola pro nevalidní hodnotu (výjimka se má vyvolat)
    if invalid is not None:
        invalid_args, invalid_kwargs = invalid
        return assert_raises(
            func,
            *invalid_args,
            exception_type=exception_type,
            expected=expected,
            **invalid_kwargs,
        )

    # 3. Fallback None
    return None