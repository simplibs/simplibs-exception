from typing import Any
from simplibs.sentinels import UNSET
from ..assert_fields import assert_exception_fields


def assert_exception_class_defaults(
    subtests: Any,
    exc_class: type[Any],
    *,
    exact_match: bool = True,
    verbose: bool = True,
    intro: str = "test_class_defaults::",
) -> Any:
    """Assert that an exception class correctly applies its default field values.

    Instantiates the exception class without constructor arguments and verifies
    that the resulting instance contains the same values as those defined on the
    class itself.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to validate.
        exact_match: Enables fuzzy string matching when False.
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The instantiated and validated exception object.
    """

    subintro = "test_class_defaults::"

    class_dict = exc_class.__dict__

    exc = exc_class()

    return assert_exception_fields(
        subtests,
        exc,

        error_name=class_dict.get("error_name", UNSET),
        label=class_dict.get("label", UNSET),
        message=class_dict.get("message", UNSET),
        expected=class_dict.get("expected", UNSET),
        value=class_dict.get("value", UNSET),
        problem=class_dict.get("problem", UNSET),
        context=class_dict.get("context", UNSET),
        how_to_fix=class_dict.get("how_to_fix", UNSET),
        exception=class_dict.get("exception", UNSET),
        get_location=class_dict.get("get_location", UNSET),
        skip_locations=class_dict.get("skip_locations", UNSET),
        oneline=class_dict.get("oneline", UNSET),

        exact_match=exact_match,
        verbose=verbose,
        intro=intro+subintro,
    )