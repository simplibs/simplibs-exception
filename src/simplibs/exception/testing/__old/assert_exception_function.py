from typing import Any, Callable, Type
import pytest
from simplibs.sentinels import UNSET, UnsetType
# Inners
from ._helpers.assertions import check_exception_fields, manage_param
from ._helpers.common import maybe_subtest


def assert_exception_function(
    subtests: Any,
    func: Callable[..., Any],
    *,
    valid_param: Any = UNSET,
    invalid_param: Any = UNSET,
    exception_type: Type[BaseException],
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
) -> Any:
    """Validate execution boundaries of a function by intercepts and field audits.

    This public testing utility orchestrates functional pipeline verifications. If provided,
    it executes a preliminary sanity check with a valid payload ensuring zero errors, 
    followed by an isolated intercept gate (`pytest.raises`) checking that an invalid payload 
    triggers the correct target exception. Finally, it audits the captured exception fields.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        func: The target callable validation or logic function under test.
        valid_param: An optional parameter payload (scalar, tuple, list, or dict) expected to 
            pass execution without raising any exception.
        invalid_param: The parameter payload (scalar, tuple, list, or dict) expected to breach 
            validation rules and trigger the target exception.
        exception_type: The expected type blueprint of the raised exception.
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

    Returns:
        The caught, instantiated exception object for further custom client assertions.
    """

    with maybe_subtest(subtests, name="test_callable", verbose=verbose):
        assert callable(func)

    # 1. Execute the optional positive verification pass (Happy Path)
    if valid_param is not UNSET:
        args, kwargs = manage_param(valid_param)
        with maybe_subtest(subtests, name="test_valid_input", verbose=verbose):
            func(*args, **kwargs)

    # 2. Prepare arguments and execute the negative intercept gate (Sad Path)
    args, kwargs = manage_param(invalid_param)

    with maybe_subtest(subtests, name="test_raises_exception", verbose=verbose):
        with pytest.raises(exception_type) as exc_info:
            func(*args, **kwargs)

    exc = exc_info.value

    # 3. Forward the caught exception instance to the properties validator
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
    )

    return exc


_DESIGN_NOTES = """
# assert_exception_function (Public Intercept & State Auditor)

## Purpose
A primary public testing interface engineered to validate functional entry points (such as validators, 
parsers, or business logic hooks) that are designed to fail under certain criteria. It unifies input 
unpacking, execution interception, and thorough telemetry auditing into a single declarative operation.

## Execution Sequence Architecture
- **Callable Verification:** Confirms the target logic hook can be securely executed.
- **Optional Happy Path Pass:** If `valid_param` is provided, the function runs natively. Any failure 
  here aborts the block early, flagging a false-positive setup error.
- **Interception Gate:** Unpacks `invalid_param` via `manage_param`, registers a `pytest.raises` isolation 
  frame, traps the raised exception, and verifies its sub-typing context.
- **Telemetry Inspection:** Forwards the captured live exception instance directly to `check_exception_fields` 
  for precise attribute validation.

## Practical Usage Examples

### Example 1: Standard Validation Function Audit
```python
def test_port_validator_logic(subtests):
    # Verifies both valid entry bounds and precise exception telemetry structure
    assert_exception_function(
        subtests,
        validate_port_range,
        valid_param=8080,
        invalid_param=99999,
        exception_type=SimpleExceptionSettingsError,
        error_name="invalid_port_range",
        value=99999,
        exact_match=True
    )

```

### Example 2: Complex Dictionary Named Parameter Unpacking

```python
def test_user_creation_restrictions(subtests):
    # Pass dictionaries as configuration blocks; manage_param handles keyword arguments automatically
    assert_exception_function(
        subtests,
        register_new_user,
        valid_param={"username": "john_doe", "age": 25},
        invalid_param={"username": "admin", "age": 12},
        exception_type=SimpleExceptionModeError,
        error_name="blacklist_username_violation",
        expected="Non-system reserved username"
    )

```

"""
