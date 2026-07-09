from typing import Any, Type
from simplibs.sentinels import UNSET, UnsetType
# Inners
from ._helpers.assertions import check_exception_fields


def assert_exception_class(
    subtests: Any,
    exc_class: Type[Any],
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
    """Instantiate a target exception class and execute validation on its telemetry fields.

    This public testing utility triggers raw instantiation of a compliant exception class
    using provided testing parameters and forwards the generated instance to the internal
    field auditor. It does not wrap execution in intercept gates (`pytest.raises`).

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: The target exception class blueprint to be tested (subclass of SimpleExceptionData).
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
        intro: Custom namespace prefix string attached to subtest names for better trace grouping.
            Defaults to "".

    Returns:
        The fully populated, instantiated exception object for further custom client assertions.
    """

    # 1. Isolate and construct the exception instance with defensive sentinel fallbacks
    exc = exc_class(
        message=message if message is not UNSET else None,
        value=value if value is not UNSET else UNSET,
        label=label if label is not UNSET else None,
        expected=expected if expected is not UNSET else None,
        problem=problem if problem is not UNSET else None,
        context=context if context is not UNSET else None,
        how_to_fix=how_to_fix if how_to_fix is not UNSET else None,
        error_name=error_name if error_name is not UNSET else None,
        exception=exception if exception is not UNSET else None,
        get_location=get_location if get_location is not UNSET else None,
        skip_locations=skip_locations if skip_locations is not UNSET else None,
        oneline=oneline if oneline is not UNSET else False,
    )

    # 2. Delegate the instantiated object to the multi-point properties verification engine
    check_exception_fields(
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
        intro=intro,
    )

    return exc


_DESIGN_NOTES = """
# assert_exception_class (Public Class State Verifier)

## Purpose
A primary public testing interface designed to verify the initialization integrity and data assignment 
correctness of individual exception classes. It serves as a direct state-inspector that programmatically 
builds an error instance and audits its internal data layout without invoking intercept mechanisms.

## Operational Scenario & Benefits
Unlike functional validators that expect a crash to happen, `assert_exception_class` is tailored for 
auditing static properties, default configuration configurations, or custom exception sub-types. 

By returning the instantiated exception object back to the test file, it allows developers to string 
together custom multi-stage validations (e.g., verifying rendering string transformations or custom attributes 
not mapped by the core protocol).

## Practical Usage Examples

### Example 1: Verifying Custom Exception Classes with Static Defaults
```python
def test_user_not_found_error_defaults(subtests):
    # Verifies that UserNotFoundError initializes its static attributes correctly
    assert_exception_class(
        subtests,
        UserNotFoundError,
        error_name="user_not_found",
        label="Database Boundary Error",
    )

```

### Example 2: Progressive Multi-Stage Assertion Blocks

```python
def test_complex_exception_payload(subtests):
    # 1. Automate standard diagnostics check
    exc = assert_exception_class(
        subtests,
        SimpleExceptionSettingsError,
        message="Invalid port provided",
        value=99999,
        expected="Valid port index between 1-65535"
    )

    # 2. Run post-validation custom extensions directly on the returned object
    assert "99999" in str(exc)
    assert exc.value > 65535

```

"""