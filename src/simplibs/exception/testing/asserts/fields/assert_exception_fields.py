from typing import Any
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ...tools import maybe_subtest, Param
# Inners
from ._utils import compare_strings


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
    # Comparison control
    exact_match: bool = False,
    startswith: bool = False,
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
            exact_match: If True, performs strict equality comparison.
            startswith: If True, validates that the actual value starts with the expected value.
            verbose: Enables pytest subtests for individual field checks.
            intro: Optional prefix for generated subtest names.

        Returns:
            The validated exception instance.
        """

    if error_name is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_error_name", verbose=verbose):
            compare_strings(error_name, exc.error_name, exact_match=exact_match, startswith=startswith)

    if label is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_label", verbose=verbose):
            compare_strings(label, exc.label, exact_match=exact_match, startswith=startswith)

    if message is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_message", verbose=verbose):
            compare_strings(message, exc.message, exact_match=exact_match, startswith=startswith)

    if expected is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_expected", verbose=verbose):
            compare_strings(expected, exc.expected, exact_match=exact_match, startswith=startswith)

    if value is not UNSET:
        value = value.value if isinstance(value, Param) else value
        with maybe_subtest(subtests, name=f"{intro}test_value", verbose=verbose):
            assert value == exc.value

    if problem is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_problem", verbose=verbose):
            compare_strings(problem, exc.problem, exact_match=exact_match, startswith=startswith)

    if context is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_context", verbose=verbose):
            compare_strings(context, exc.context, exact_match=exact_match, startswith=startswith)

    if how_to_fix is not UNSET:
        with maybe_subtest(subtests, name=f"{intro}test_how_to_fix", verbose=verbose):
            compare_strings(how_to_fix, exc.how_to_fix, exact_match=exact_match, startswith=startswith)

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


_DESIGN_NOTES = """
# assert_exception_fields (Granular Telemetry Assertion Blade)

## Purpose
Acts as the dedicated, single-responsibility telemetry validator for instantiated exception instances. 
The flat execution structure ensures immediate visual parity across all property checks, 
facilitating rapid diagnostic auditing.

## Operational Modalities
1. **Direct Standalone Verification:** Invoked by end-users auditing properties on an already caught exception instance.
2. **Class Facade Assembly:** Leveraged by `assert_exception_class` engines to verify default metadata properties populated during initialization.
3. **Functional Facade Assembly:** Leveraged by `assert_exception_function` chains to deep-check operational parameters on errors raised dynamically.

## Comparison Hierarchy
The engine routes string-based attributes through a multi-modal comparator supporting:
- **Exact Match:** Strict equality verification.
- **Starts With:** Prefix-based validation (ideal for dynamic backtraces).
- **Substring Inclusion:** Default fuzzy-match logic.

## Sentinel Protection Design
Defaults to `UNSET` to allow selective validation. This explicitly distinguishes between 
skipping an evaluation (`UNSET`) and asserting an explicit empty state (`None`/`""`).

Additionally, the interface features an implicit unpacking mechanism for the `value` property: 
if it encounters an explicit `Param` token, it transparently unwraps the inner data node before 
comparison. This eliminates defensive type-checking logic from high-level test matrix suites.
"""