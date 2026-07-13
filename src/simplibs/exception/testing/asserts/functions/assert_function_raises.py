"""
Assertion utility for validating negative functional execution boundaries.
"""
from typing import Any, Callable
import pytest
from simplibs.sentinels import UNSET, UnsetType

# Outers
from ...tools import maybe_subtest, Kwargs
# Inners
from ._utils import process_params


def assert_function_raises(
    subtests: Any,
    func: Callable[..., Any],
    *,
    invalid_params: tuple[Any, ...] | Kwargs,
    exception_type: (
        type[BaseException]
        | tuple[type[BaseException], ...]
        | UnsetType
    ) = UNSET,
    verbose: bool = True,
    intro: str = "",
) -> BaseException:
    """Assert that a function raises an exception when invoked with invalid parameters.

    Normalizes the invalid parameter block, invokes the target callable, and verifies
    that an exception is triggered. Optionally validates the exact type of the raised
    exception against an expected type or tuple of types.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        func: The target function or callable under test.
        invalid_params: The explicit parameter payload (tuple or Kwargs) designed
            To trigger an execution failure.
        exception_type: Expected exception class or a tuple of valid exception classes.
            If UNSET, any exception deriving from BaseException satisfies the check.
        verbose: Enables isolated pytest subtest logging layout tracking.
        intro: Optional prefix string added to the generated subtest identity name.

    Returns:
        The caught exception instance for downstream field inspection.
    """
    # Extract standard execution components (*args, **kwargs) from the input wrapper
    args, kwargs = process_params(invalid_params)

    # 1. Verify that the function boundary execution successfully forces an exception drop
    with maybe_subtest(
        subtests,
        name=f"{intro}test_raises_exception",
        verbose=verbose,
    ):
        with pytest.raises(BaseException) as exc_info:
            func(*args, **kwargs)

    # Safely extract the literal exception instance captured by the pytest engine
    exc = exc_info.value

    # 2. Verify that the triggered exception matches the specific expected type mapping
    if exception_type is not UNSET:
        # Framework Guard: If the raised error type is fundamentally unexpected (e.g., a native TypeError
        # caused by bad signature mapping), we must issue a hard-fail immediately. Continuing into
        # downstream telemetry checks would trigger misleading AttributeError chains on the native error object.
        exception_type: type[BaseException] | tuple[type[BaseException], ...]
        if not isinstance(exc, exception_type):
            expected_names = (
                exception_type.__name__
                if isinstance(exception_type, type)
                else ", ".join(t.__name__ for t in exception_type)
            )
            pytest.fail(
                f"\n[Framework Guard] Target function raised an unexpected exception type!\n"
                f"Expected: {expected_names}\n"
                f"Actual:   {type(exc).__name__} ({exc})\n\n"
                f"💡 Tip: If you received an unexpected TypeError or failure, verify your signatures. "
                f"Remember that all operational payloads must be strictly wrapped inside a tuple: "
                f"invalid_params=(value,) or Kwargs instance."
            )

        # Re-verify within the subtest context for standard report logging
        with maybe_subtest(
            subtests,
            name=f"{intro}test_exception_type",
            verbose=verbose,
        ):
            exception_type: type[BaseException] | tuple[type[BaseException], ...]
            assert isinstance(exc, exception_type)

    return exc


_DESIGN_NOTES = """
# assert_function_raises (Negative Boundary Assertion Blade)

## Purpose
An automated validation utility for negative functional constraints. It wraps parameter normalization, 
guaranteed exception interception, and strict type verification into a clean, reusable interface.

## Execution Sequencing & Exception Capture
1. **Parameter Unpacking Layer:** Leverages `process_params` to seamlessly transform explicit argument 
   tuples or standalone `Kwargs` configurations into strict runtime `*args` and `**kwargs`.
2. **Interception Guard (`pytest.raises`):** Forces the core execution block inside a master 
   Python `BaseException` net. Because this guard is nested directly inside the bi-modal 
   `maybe_subtest` engine, it handles failure state analysis consistently across both verbose and fast-pass CI lanes.
3. **Framework Guard & Type Blueprint Matching:** Extracts the underlying instance (`exc_info.value`) 
   An performs a pre-flight lineage validation. If the caught error diverges from `exception_type`, 
   The engine actively aborts execution using `pytest.fail`. This hard stop prevents cascading, 
   Unreadable `AttributeError` exceptions from running inside subsequent field-telemetry blocks 
   When a function unexpectedly throws standard runtime signature errors (e.g., a native `TypeError` 
   Due to parameter mismatch).

## Downstream Fluid Interface Design
By returning the raw caught `BaseException` instance, this function acts as an ideal conduit for 
fluid assertions. The output can be piped directly into telemetry inspection blades (such as `assert_exception_fields`), 
enabling developers to validate deep error messages, codes, or dynamic hints raised from deep within the functional context.
"""