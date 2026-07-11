"""

1. assert_exception_class_constructor()

Úkol této funkce by měl být jediný:

"Konstruktor přijímá všechny parametry a správně je propisuje do instance."

Tato funkce v sobě prakticky obsahuje dnešní assert_exception_class().

assert_exception_class_constructor()
│
├── vytvoř instanci
└── assert_exception_fields()

Takže její logika by byla:

exc = exc_class(...)

assert_exception_fields(...)

return exc

To je vše.
"""

def assert_exception_class_constructor(
    subtests: Any,
    exc_class: type[Any],
    *,
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
    intro: str = "",
) -> Any:
    """Assert that an exception constructor accepts and stores all supported fields.

    Instantiates the exception class using the supplied constructor arguments and
    verifies that every provided value has been correctly propagated to the
    resulting exception instance.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to instantiate.
        error_name: Expected value of ``exc.error_name``.
        label: Expected value of ``exc.label``.
        message: Expected value of ``exc.message``.
        expected: Expected value of ``exc.expected``.
        value: Expected value of ``exc.value``.
        problem: Expected value of ``exc.problem``.
        context: Expected value of ``exc.context``.
        how_to_fix: Expected value of ``exc.how_to_fix``.
        exception: Expected value of ``exc.exception``.
        get_location: Expected value of ``exc.get_location``.
        skip_locations: Expected value of ``exc.skip_locations``.
        oneline: Expected value of ``exc.oneline``.
        exact_match: Enables fuzzy string matching when False.
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The instantiated and validated exception object.
    """

    exc = exc_class(
        message=message if message is not UNSET else None,
        value=value if value is not UNSET else UNSET,
        label=label if label is not UNSET else None,
        expected=expected if expected is not UNSET else None,
        problem=problem if problem is not UNSET else None,
        context=context if context is not UNSET else None,
        how_to_fix=how_to_fix if how_to_fix is not UNSET else None,
        error_name=error_name if error_name is not UNSET else None,
        exception=exception if exception is not UNSET else None,
        get_location=get_location if get_location is not UNSET else None,
        skip_locations=skip_locations if skip_locations is not UNSET else None,
        oneline=oneline if oneline is not UNSET else False,
    )

    return assert_exception_fields(
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
        intro=intro,
    )