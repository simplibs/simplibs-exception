from typing import Any
from .._helpers import maybe_subtest


def assert_exception_class_interface(
    subtests: Any,
    exc_class: type[Any],
    *,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Assert that an exception class exposes the expected public interface.

    Instantiates the exception class and verifies the availability and basic
    functionality of the standard public API.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to validate.
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The instantiated exception object.
    """
    subintro = "test_class_interface::"

    exc = exc_class()

    with maybe_subtest(
        subtests,
        name=f"{intro}test_str",
        verbose=verbose,
    ):
        assert isinstance(str(exc), str)

    with maybe_subtest(
        subtests,
        name=f"{intro}test_repr",
        verbose=verbose,
    ):
        assert isinstance(repr(exc), str)

    with maybe_subtest(
        subtests,
        name=f"{intro}test_to_dict",
        verbose=verbose,
    ):
        assert isinstance(exc.to_dict(), dict)

    with maybe_subtest(
        subtests,
        name=f"{intro}test_to_debug_dict",
        verbose=verbose,
    ):
        assert isinstance(exc.to_debug_dict(), dict)

    with maybe_subtest(
        subtests,
        name=f"{intro}test_to_json",
        verbose=verbose,
    ):
        assert isinstance(exc.to_json(), str)

    return exc