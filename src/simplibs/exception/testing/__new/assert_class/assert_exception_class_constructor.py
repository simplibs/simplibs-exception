from typing import Any
from ..assert_fields import assert_exception_fields
from .._helpers import maybe_subtest


def assert_exception_class_constructor(
    subtests: Any,
    exc_class: type[Any],
    *,
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
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The instantiated and validated exception object.
    """
    subintro = "test_class_constructor::"

    exc = exc_class(
        message="<message>",
        value="<value>",
        label="<label>",
        expected="<expected>",
        problem="<problem>",
        context="<context>",
        how_to_fix="<how_to_fix>",
        error_name="<ERROR_NAME>",
        exception=ValueError("test exception"),
        get_location=False,
        skip_locations=("<skip_locations>",),
        oneline=True,
    )

    assert_exception_fields(
        subtests,
        exc,

        error_name=exc.error_name,
        label=exc.label,
        message=exc.message,
        expected=exc.expected,
        value=exc.value,
        problem=exc.problem,
        context=exc.context,
        how_to_fix=exc.how_to_fix,
        exception=exc.exception,
        get_location=exc.get_location,
        skip_locations=exc.skip_locations,
        oneline=exc.oneline,

        exact_match=True,
        verbose=verbose,
        intro=intro+subintro,
    )