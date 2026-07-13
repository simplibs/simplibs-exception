"""
Composite orchestrator for functional execution boundaries and exception telemetry audits.
"""
from typing import Any, Callable
from simplibs.sentinels import UNSET, UnsetType

# Outers
from .tools import Kwargs
# Inners
from .asserts.fields import assert_exception_fields
from .asserts.functions import (
    assert_function_callable,
    assert_function_raises,
    assert_function_valid_input
)


def assert_exception_function(
    # Required parameters:
    subtests: Any,
    func: Callable[..., Any],
    *,
    exception_type: type[BaseException],
    invalid_params: tuple[Any, ...] | Kwargs,
    # Optional parameters:
    valid_params: tuple[Any, ...] | Kwargs | UnsetType = UNSET,
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
    # Setting parameters:
    exact_match: bool = False,
    startswith: bool = False,
    verbose: bool = True,
    intro: str = "",
    deep_check: bool = True,
) -> BaseException:
    """Validate execution boundaries of a function by intercepts and field audits.

    This public testing utility orchestrates functional pipeline verifications. If provided,
    it executes a preliminary sanity check with a valid payload ensuring zero errors,
    followed by an isolated intercept gate (`pytest.raises`) checking that an invalid payload
    triggers the correct target exception. Finally, it audits the captured exception fields.

    Args:
        [Required parameters]
        subtests: The native pytest subtests fixture manager instance.
        func: The target callable validation or logic function under test.
        exception_type: The expected type blueprint of the raised exception.
        invalid_params: The explicit parameter payload (tuple or Kwargs) expected
            to trigger the target exception.
        [Optional parameters]
        valid_params: An optional explicit parameter payload (tuple or Kwargs) expected
            to pass without error.
        error_name: Expected internal system error identity code.
        label: Expected human-readable categorization title.
        message: Expected dynamic text body or terminal explanation block.
        expected: Expected value or state description criteria that was breached.
        value: Expected raw problematic value or object state.
        problem: Expected breakdown sequence or root cause description.
        context: Expected technical parameters or diagnostic environmental metrics.
        how_to_fix: Expected structured actionable recommendations.
        exception: Expected raw intercept nested exception instance.
        get_location: Expected active relative stack scanning frame trace.
        skip_locations: Expected global or contextual exclusion string path filter.
        oneline: Expected strict structural flag enforcing flat single-line message.
        [Setting parameters]
        exact_match: If True, enforces strict exact string equality.
        startswith: If True, validates that the actual value starts with the expected value.
        verbose: If True, registers individual telemetry property checks as subtests.
        intro: Optional prefix string added to the generated subtest identity name.
        deep_check: If True, triggers advanced explicit telemetry field inspection.

    Returns:
        The caught, instantiated exception object.
    """
    # 1. Verify that the target under audit is an executable object
    assert_function_callable(subtests, func, verbose=verbose, intro=intro)

    # 2. Sanity check: Execute positive pipeline if valid_params is provided
    if valid_params is not UNSET:
        # noinspection PyTypeChecker
        assert_function_valid_input(
            subtests,
            func,
            valid_params=valid_params,
            verbose=verbose,
            intro=intro
        )

    # 3. Intercept execution failure and capture the triggered framework exception
    exc = assert_function_raises(
        subtests,
        func,
        invalid_params=invalid_params,
        exception_type=exception_type,
        verbose=verbose,
        intro=intro
    )

    # 4. Perform localized granular telemetry deep checking if enabled
    if deep_check:
        assert_exception_fields(
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
            startswith=startswith,
            verbose=verbose,
            intro=intro
        )

    return exc


_DESIGN_NOTES = """
# assert_exception_function (Composite Functional Boundary Auditor)

## Purpose
Implements a clean Facade Pattern that orchestrates functional validation pipelines. It synchronizes 
positive execution sanity passes, defensive exception interception, and intensive telemetry 
property checking into a unified, single-invocation testing matrix.

## Parametric Contract Boundaries
Following the framework-wide strict signatures policy, both `invalid_params` and `valid_params` 
accept explicit argument structures consisting of a positional tuple (representing `*args`) 
or a standalone `Kwargs` configuration wrapper.

## Comparison Modalities (Opt-in Architecture)
The engine defaults to substring inclusion (`in` operator), which provides the most resilient 
audit for dynamic error messages. Stricter validation modes are available via explicit flags:
- **`exact_match=True`**: Forces full-string equality (useful for static error codes).
- **`startswith=True`**: Forces prefix-based validation (useful for messages with dynamic suffixes).

## Refactored Operational Flow
The execution sequence builds a progressive evaluation matrix:
1. Callable Isolation Gate -> 2. Happy Path Clearance -> 3. Negative Intercept Gate -> 4. Deep Telemetry Evaluation.

## `deep_check` Intent Scope Calibration
`deep_check` is scoped to wrap the exhaustive attribute inspection layer.
- **`True` (Default):** Full compliance audit, validating both exception type and diagnostic message precision.
- **`False`:** High-speed smoke testing, validating only the exception boundary signature.
"""