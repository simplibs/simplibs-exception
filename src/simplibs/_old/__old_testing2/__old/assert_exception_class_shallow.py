from typing import Any
from simplibs.sentinels import UnsetType, UNSET

from .assert_class import (
    assert_exception_class_defaults,
    assert_exception_class_constructor,
    assert_exception_class_interface,
    assert_exception_class_inheritance
)


def assert_exception_class(
    subtests: Any,
    exc_class: type[Any],
    *,
    verbose: bool = False,
) -> Any:
    """Execute a complete validation suite for an exception class.

    Runs all available structural, constructor, default-value, and interface
    checks against the supplied exception class.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to validate.

        exact_match: Enables fuzzy comparison when False.
        verbose: Enables pytest subtests.
        intro: Optional prefix for generated subtest names.

    Returns:
        The validated exception class instance.
    """

    # 1. Verify inheritance contract
    assert_exception_class_inheritance(
        subtests,
        exc_class,
        verbose=verbose,
    )

    exc = exc_class()

    assert isinstance(exc, BaseException)

