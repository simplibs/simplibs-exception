from typing import Any, Literal
from simplibs.sentinels import UNSET


def bool_or_exception(
    return_bool: bool,
    *,
    message: str | None = None,
    value: Any = UNSET,
    label: str | None = None,
    expected: str | None = None,
    problem: str | tuple[str, ...] | list[str] | None = None,
    context: str | tuple[str, ...] | list[str] | None = None,
    how_to_fix: str | tuple[str, ...] | list[str] | None = None,
    error_name: str | None = None,
    exception: Exception | type[Exception] | None = None,
    get_location: bool | int | None = None,
    skip_locations: tuple[str, ...] | str | None = None,
    oneline: bool = False,
) -> Literal[False]:
    """Returns False or raises SimpleException — a shortcut for conditional validation routines.

    Args:
        return_bool: If True, intercepts execution and returns False immediately.
                     If False, raises a configured SimpleException.
        message: Custom error message override.
        value: The evaluated payload that triggered the failure.
        label: The name of the field, property, or context being validated.
        expected: A clear description of the valid layout or type constraints.
        problem: Precise description of what failed in the current state.
        context: Broader execution state or diagnostic details.
        how_to_fix: Actionable steps for the developer to resolve the issue.
        error_name: Custom dynamic class name override for the exception.
        exception: Foreign exception to link or inherit from.
        get_location: Controls the stack-trace caller-site resolution depth.
        skip_locations: Custom patterns to exclude during location resolution.
        oneline: If True, forces ultra-compact single-line log-style output.

    Returns:
        Literal[False]: Always returns False if return_bool is active.

    Raises:
        SimpleException: If return_bool is False.
    """
    # 1. Short-circuit and return False if a boolean fallback is explicitly requested
    if return_bool:
        return False

    # 2. Offset explicit integer locations to account for this helper layer context
    if isinstance(get_location, int):
        get_location += 1

    # 3. Lazy-load SimpleException inside the execution block to dismantle package circular dependencies
    from ..SimpleException import SimpleException

    # 4. Fire the structured exception down the execution stream
    raise SimpleException(
        message=message,
        value=value,
        label=label,
        expected=expected,
        problem=problem,
        context=context,
        how_to_fix=how_to_fix,
        error_name=error_name,
        exception=exception,
        get_location=get_location,
        skip_locations=skip_locations,
        oneline=oneline,
    )


_DESIGN_NOTES = """
# bool_or_exception

## Purpose
A specialized operational shortcut optimized for data validation pipelines. It standardizes the 
common defensive pattern where guardrails must either gracefully fail by returning a boolean state 
indicator (`False`) or immediately terminate execution by throwing a rich error panel.

## Code Pattern Comparison

### Standard Layout (Without helper)
```python
if not is_valid:
    if return_bool:
        return False
    raise SimpleException(
        label="parameter age",
        expected="positive integer",
    )
return True

```

### Consolidated Layout (With helper)

```python
if not is_valid:
    return bool_or_exception(
        return_bool,
        label="parameter age",
        expected="positive integer",
    )
return True

```

## Explicit Signature Model

The keyword-only (`*`) configuration enforces full explicit parameter passing. This enables robust
IDE autocomplete reflection, strict type-checking, and static analysis visibility across the boundary layer.

## Location Offset Handling (Stack-Frame Continuity)

The entire internal module package space (`simplibs/exception`) is protected by default via the
framework-wide `_SYSTEM_BLACKLIST`. As a result, standard execution tracking (`get_location=True/None`)
automatically bypasses this helper frame without manual macro manipulation.

However, if a developer passes a specific relative integer offset depth (e.g., `get_location=2`),
the integer must be incremented by `+1` to shift the reference calibration vector beyond this
intermediary tool wrapper context, preserving perfect call-site alignment.

## Defeating Circular Import Locks

The module layout creates a natural architectural cross-dependency: `SimpleException` relies on low-level
utility tooling, while this diagnostic helper must construct a `SimpleException` instance.

To remain completely decoupled without resorting to global runtime hacks, `SimpleException` is imported
via a lazy execution-time pattern directly inside the failure branch. Since this branch is only
entered when `return_bool=False`, the rest of the ecosystem is guaranteed to be fully compiled in memory,
guaranteeing clean initialization phases.
"""