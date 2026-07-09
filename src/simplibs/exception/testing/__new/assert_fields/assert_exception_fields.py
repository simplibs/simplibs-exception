from typing import Any
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .._helpers import maybe_subtest, compare_strings


def assert_exception_fields(
    subtests: Any,
    exc: Any,
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
    """Assert that an exception instance contains the expected field values.

    Compares selected exception attributes against the expected values provided
    to this function. Only parameters that are not UNSET are validated.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc: The exception instance to validate.
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
        exact_match: If False, string values are compared using substring matching.
        verbose: Enables pytest subtests for individual field checks.
        intro: Optional prefix for generated subtest names.

    Returns:
        The validated exception instance.
    """

    if error_name is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_error_name", verbose=verbose):
            compare_strings(error_name, exc.error_name, exact_match=exact_match)

    if label is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_label", verbose=verbose):
            compare_strings(label, exc.label, exact_match=exact_match)

    if message is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_message", verbose=verbose):
            compare_strings(message, exc.message, exact_match=exact_match)

    if expected is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_expected", verbose=verbose):
            compare_strings(expected, exc.expected, exact_match=exact_match)

    if value is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_value", verbose=verbose):
            assert value == exc.value

    if problem is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_problem", verbose=verbose):
            compare_strings(problem, exc.problem, exact_match=exact_match)

    if context is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_context", verbose=verbose):
            compare_strings(context, exc.context, exact_match=exact_match)

    if how_to_fix is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_how_to_fix", verbose=verbose):
            compare_strings(how_to_fix, exc.how_to_fix, exact_match=exact_match)

    if exception is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_exception", verbose=verbose):
            assert exception == exc.exception

    if get_location is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_get_location", verbose=verbose):
            assert get_location == exc.get_location

    if skip_locations is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_skip_locations", verbose=verbose):
            assert skip_locations == exc.skip_locations

    if oneline is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_oneline", verbose=verbose):
            assert oneline == exc.oneline

    return exc