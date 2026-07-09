from typing import Any
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ..common import maybe_subtest
# Inners
from .compare_strings import compare_strings


def check_exception_fields(
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
) -> None:
    """Validate captured exception state attributes against expected criteria.

    Compares the runtime values present within an exception instance against explicitly
    provided evaluation metrics, routing validations through safe string comparators
    and subtest boundary managers.
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


_DESIGN_NOTES = """
# check_exception_fields (Internal State Validator)

## Purpose
An internal data-integrity validation utility designed to audit the complete state matrix of a 
`SimpleException` instance. It acts as a specialized multi-point inspector verifying that 
diagnostic fields match user expectations without altering or ignoring raw context states.

## Sentinel-Driven Selective Evaluation
By defaulting parameters to a strict `UNSET` singleton (`UnsetType`), the validator supports partial 
or specific telemetry state auditing. Fields that match `UNSET` are skipped, allowing test writers 
to target individual properties (e.g., verifying just the `error_name` or `value`) without being 
forced to supply expectations for every other concurrent field.

## Execution Isolation & String Matching
Every active check block routes through a conditional `maybe_subtest` context layer using a configurable 
`intro` text prefix namespace. String attributes (including sequences like `problem` or `context` logs) 
are processed via `compare_strings` to seamlessly handle fuzzy/exact matching conditions. Primitives, 
class types, and configurations route through native strict assertions.
"""