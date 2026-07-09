from typing import Any
from .._helpers import maybe_subtest
from ....SimpleExceptionData import  SimpleExceptionData


def assert_exception_class_inheritance(
    subtests: Any,
    exc_class: type[Any],
    *,
    verbose: bool = True,
    intro: str = "",
) -> type[Any]:
    """Assert that an exception class satisfies the required inheritance contract.

    Verifies that the supplied class derives from both ``BaseException`` and
    ``SimpleExceptionData``.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to validate.
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The validated exception class.
    """

    subintro = "test_class_inheritance::"

    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_base_exception_inheritance",
        verbose=verbose,
    ):
        assert issubclass(exc_class, BaseException)

    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_simple_exception_data_inheritance",
        verbose=verbose,
    ):
        assert issubclass(exc_class, SimpleExceptionData)

    return exc_class