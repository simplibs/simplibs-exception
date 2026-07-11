from typing import Any, NoReturn

from ...._core_logic.internal_exceptions import SimpleExceptionSettingsError


def raise_unsupported_kwargs_parameter(
    instance: Any,
    args: tuple[Any, ...],
) -> NoReturn:
    """Explicitly raise a diagnostics error when Kwargs initialization parameters are malformed.

    Differentiates between multiple positional arguments or invalid mapping types to
    provide clear actionable recovery steps to the test writer.
    """
    label = f"{type(instance).__name__} validation"

    # Branch 1: Too many positional arguments passed to the wrapper
    if len(args) > 1:
        raise SimpleExceptionSettingsError(
            value=args,
            label=label,
            problem=f"The wrapper accepts at most one positional mapping argument, received {len(args)}.",
            how_to_fix=(
                "Group multiple keyword arguments as a single dictionary: Kwargs({'a': 1, 'b': 2})",
                "Or pass them directly as named parameters: Kwargs(a=1, b=2)",
            ),
        )

    # Branch 2: Singular positional argument is not a valid Mapping
    raise SimpleExceptionSettingsError(
        value=args[0] if args else None,
        label=label,
        problem=f"Expected a valid collections.abc.Mapping structure, received '{type(args[0]).__name__}'.",
        how_to_fix=(
            "Ensure the positional argument implements the Mapping interface (e.g., a native dict).",
            "Primitives, lists, or tuples cannot be expanded into keyword arguments.",
        ),
    )


_DESIGN_NOTES = """
# raise_unsupported_kwargs_parameter

## Purpose
A specialized internal execution stopper designed to protect the `Kwargs` wrapper initialization matrix. 
By isolating exception building from the wrapper constructor, it maximizes runtime clarity and keeps 
the core dataclass definition lightweight.

## Error Diagnostics Routing
The function analyzes the provided arguments tuple to isolate the exact developer mistake:
1. **Multi-Argument Overflow:** Triggered when more than one positional collection is supplied.
2. **Invalid Type Inversion:** Triggered when the single positional element fails the `Mapping` interface check.

Both paths leverage `SimpleExceptionSettingsError` to emit comprehensive, structured remediation logs.
"""