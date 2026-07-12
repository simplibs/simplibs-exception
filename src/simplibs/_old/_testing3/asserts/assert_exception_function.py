from typing import Any, Callable
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .fields import assert_exception_fields
from .functions import (
    assert_function_callable,
    assert_function_raises,
    assert_function_valid_input
)


def assert_exception_function(
    subtests: Any,
    func: Callable[..., Any],
    *,
    exception_type: type[BaseException],
    invalid_param: Any,
    valid_param: Any = UNSET,
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
    deep_check: bool = True,
) -> BaseException:
    """Validate execution boundaries of a function by intercepts and field audits.

    This public testing utility orchestrates functional pipeline verifications. If provided,
    it executes a preliminary sanity check with a valid payload ensuring zero errors,
    followed by an isolated intercept gate (`pytest.raises`) checking that an invalid payload
    triggers the correct target exception. Finally, it audits the captured exception fields.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        func: The target callable validation or logic function under test.
        exception_type: The expected type blueprint of the raised exception.
        invalid_param: The parameter payload (scalar, tuple, list, or dict) expected to breach
            validation rules and trigger the target exception.
        valid_param: An optional parameter payload (scalar, tuple, list, or dict) expected to
            pass execution without raising any exception.
        error_name: Expected internal system error identity code or unique string slug.
        label: Expected human-readable categorization title or layer indicator.
        message: Expected dynamic text body or terminal explanation block.
        expected: Expected value or state description criteria that was breached.
        value: Expected raw problematic value or object state that triggered the exception.
        problem: Expected breakdown sequence or description of the concrete malfunction root causes.
        context: Expected technical parameters, surrounding values, or diagnostic environmental metrics.
        how_to_fix: Expected structured actionable recommendations or remediation walkthrough paths.
        exception: Expected raw intercept nested exception instance or underlying class type.
        get_location: Expected active relative stack scanning frame trace setting indicator.
        skip_locations: Expected global or contextual exclusion string path filter collection.
        oneline: Expected strict structural flag enforcing flat single-line message rendering layouts.
        exact_match: When True, enforces strict exact string equality. When False, switches string
            checks to fuzzy substring inclusion lookups (`expected in actual`). Defaults to True.
        verbose: If True, registers individual telemetry property checks under independent
            pytest subtest sub-keys. If False, runs inline silently at maximum speed. Defaults to True.
        intro: Optional prefix string added to the generated subtest identity name.
        deep_check: If True, triggers advanced explicit telemetry field inspection audits on the
            caught exception instance. Defaults to True.

    Returns:
        The caught, instantiated exception object for further custom client assertions.
    """

    # 1. Verify that the target under audit is an executable object (Structural check)
    assert_function_callable(
        subtests,
        func,
        verbose=verbose,
        intro=intro
    )

    # 2. Sanity check: Execute positive pipeline if a valid parameter block is provided
    if valid_param is not UNSET:
        assert_function_valid_input(
            subtests,
            func,
            valid_param=valid_param,
            verbose=verbose,
            intro=intro
        )

    # 3. Intercept execution failure and capture the triggered framework exception
    exc = assert_function_raises(
        subtests,
        func,
        invalid_param=invalid_param,
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
            verbose=verbose,
            intro=intro
        )

    return exc


_DESIGN_NOTES = """
# assert_exception_function (Composite Functional Boundary Auditor)

## Purpose
Implements a clean Facade Pattern that orchestrates functional validation pipelines. It synchronizes positive execution sanity passes, defensive exception interception, and intensive telemetry property checking into a unified, single-invocation testing matrix.

## Refactored Operational Flow & Lifecycle Architecture
The execution sequence has been streamlined to build a progressive evaluation matrix:
1. **Callable Isolation Gate:** Immediate check to ensure the target is runnable.
2. **Happy Path Clearance:** If `valid_param` is provided, it is processed *before* the failure injection. This guarantees that the target logic is inherently stable and operational before boundary breaking conditions are tested.
3. **Negative Intercept Gate:** Invokes the target with `invalid_param` and traps the escaping exception via the internal `pytest.raises` sub-module structure.
4. **Deep Telemetry Evaluation:** Evaluates the caught exception's properties against the provided metadata criteria.

## `deep_check` Intent Scope Calibration
The `deep_check` flag is intentionally scoped to wrap **only** the exhaustive attribute inspection layer (`assert_exception_fields`). 
- **`deep_check=True` (Default):** Provides end-to-end assurance, confirming both the type of the exception and the precision of its diagnostic payload text strings.
- **`deep_check=False`:** High-speed constraint validation (Smoke Testing). Useful when generating bulk mass matrices where verifying the raw exception type boundary is sufficient, while bypassing the computational and log overhead of parsing dynamic error message strings.
"""