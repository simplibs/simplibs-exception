from typing import Any, Callable
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ..assertions import assert_does_not_raise, assert_exception_fields, assert_raises


def assert_simple_exception(
    func: Callable[..., Any],
    *,
    # --- How to call the function under test ---
    valid_value: Any = UNSET,
    invalid_value: Any = UNSET,
    valid_args: tuple[Any, ...] = (),
    valid_kwargs: dict[str, Any] | None = None,
    invalid_args: tuple[Any, ...] = (),
    invalid_kwargs: dict[str, Any] | None = None,
    exception_type: type[BaseException] = Exception,
    # --- Expected SimpleExceptionData fields (UNSET = don't check this one) ---
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
) -> BaseException | None:
    """
    A complete, SimpleException/SimpleExceptionData-tailored test pipeline
    for validate_ and raise_ functions. Replaces the repetitive
    call-and-check boilerplate you'd otherwise write by hand for every
    single validator in a "validate_..." / "raise_..." style codebase:
    you call this once per function, pass in only the values you actually
    want to test, and it does the rest.

    Pipeline:
        1. `func` must be provided and callable — otherwise this fails
           immediately and loudly (never silently "passes" without
           actually testing anything).
        2. If a positive input is given (`valid_value` and/or `valid_args`
           / `valid_kwargs`), calls `func` with it and asserts it does
           NOT raise.
        3. If a negative input is given (`invalid_value` and/or
           `invalid_args` / `invalid_kwargs`), OR if no positive input was
           given at all (the typical case for a parameterless `raise_...`
           function), calls `func` with it and asserts it DOES raise
           `exception_type`.
        4. For every SimpleExceptionData field parameter below that was
           explicitly provided (i.e. is not UNSET), asserts that the
           caught exception's matching attribute equals it. Fields left
           at their default UNSET are simply not checked — including
           fields whose valid/expected value genuinely is None, False, or
           an empty tuple, since UNSET (not None) marks "don't check this".

    Args:
        func: The validate_... or raise_... function under test.
        valid_value: Convenience shortcut for `valid_args=(valid_value,)`
                     — covers the common case of a single positional
                     "value" parameter.
        invalid_value: Same shortcut, for the negative case.
        valid_args / valid_kwargs: Explicit call arguments for the
                     positive case, for functions taking more than one
                     parameter (e.g. `check_children_attributes(parent, child)`).
        invalid_args / invalid_kwargs: Same, for the negative case.
        exception_type: Expected exception type for the negative case.
        error_name, label, message, expected, value, problem, context,
        how_to_fix, exception, get_location, skip_locations, oneline:
            Expected values of the matching SimpleExceptionData attributes
            on the caught exception. Leave at the default UNSET for any
            field you don't want to verify.

    Returns:
        The caught exception from the negative case, or None if only the
        positive case was checked.

    Raises:
        AssertionError: If `func` is missing/not callable, or if any step
                        of the pipeline fails.
    """

    # 1. Ověření zda je funkce volatelný objekt
    if not callable(func):
        raise AssertionError(
            "assert_simple_exception() requires a valid, callable function "
            f"to test — got: {func!r}"
        )

    # 2. Zpracování vstupních hodnot
    valid_kwargs = valid_kwargs or {}
    invalid_kwargs = invalid_kwargs or {}

    resolved_valid_args = (
        valid_args if valid_args else
        ((valid_value,) if valid_value is not UNSET else None)
    )
    resolved_invalid_args = (
        invalid_args if invalid_args else
        ((invalid_value,) if invalid_value is not UNSET else None)
    )

    has_valid_case = resolved_valid_args is not None or bool(valid_kwargs)
    has_invalid_case = resolved_invalid_args is not None or bool(invalid_kwargs)

    # 3. Ověření validní hodnoty
    if has_valid_case:
        assert_does_not_raise(func, *(resolved_valid_args or ()), **valid_kwargs)

    # 4. Ověření nevalidní hdonoty
    # Always exercised when an invalid input was given, OR when no positive
    # input was given at all (parameterless raise_... functions).
    exc: BaseException | None = None
    if has_invalid_case or not has_valid_case:

        # 4.1 Ověření zda funkce vyvolá výjimku
        exc = assert_raises(
            func,
            *(resolved_invalid_args or ()),
            exception_type=exception_type,
            **invalid_kwargs,
        )

        # 4.2 Ověření jednotlivých položek
        field_checks = {
            "error_name": error_name,
            "label": label,
            "message": message,
            "expected": expected,
            "value": value,
            "problem": problem,
            "context": context,
            "how_to_fix": how_to_fix,
            "exception": exception,
            "get_location": get_location,
            "skip_locations": skip_locations,
            "oneline": oneline,
        }
        fields_to_check = {
            name: val for name, val in field_checks.items() if val is not UNSET
        }
        if fields_to_check:
            # noinspection PyTypeChecker
            assert_exception_fields(exc, fields_to_check)

    # 5. Navrácení výjimky
    return exc