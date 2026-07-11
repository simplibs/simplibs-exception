import pytest
from typing import Any, Callable
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ..._helpers import maybe_subtest, manage_param


def assert_function_raises(
    subtests: Any,
    func: Callable[..., Any],
    *,
    invalid_param: Any,
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
        invalid_param: The raw parameter payload designed to trigger an execution failure.
        exception_type: Expected exception class or a tuple of valid exception classes. 
            If UNSET, any exception deriving from BaseException satisfies the check.
        verbose: Enables isolated pytest subtest logging layout tracking.
        intro: Optional prefix string added to the generated subtest identity name.

    Returns:
        The caught exception instance for downstream field inspection.
    """

    # Extract standard execution components (*args, **kwargs) from the input wrapper
    args, kwargs = manage_param(invalid_param)

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
        with maybe_subtest(
            subtests,
            name=f"{intro}test_exception_type",
            verbose=verbose,
        ):
            # noinspection PyTypeChecker
            assert isinstance(exc, exception_type)

    return exc


_DESIGN_NOTES = """
# assert_function_raises (Negative Boundary Assertion Blade)

## Purpose
An automated validation utility for negative functional constraints. It wraps parameter normalization, 
guaranteed exception interception, and strict type verification into a clean, reusable interface.

## Execution Sequencing & Exception Capture
1. **Parameter Unpacking Layer:** Leverages `manage_param` to seamlessly transform scalar values, 
   sequences, or explicit `Kwargs` allocations into runtime `*args` and `**kwargs`.
2. **Interception Guard (`pytest.raises`):** Forces the core execution block inside a master 
   Python `BaseException` net. Because this guard is nested directly inside the bi-modal 
   `maybe_subtest` engine, it handles failure state analysis consistently across both verbose and fast-pass CI lanes.
3. **Type Blueprint Matching:** Extracts the underlying instance (`exc_info.value`) and checks its 
   lineage via `isinstance`. By keeping this check independent from the initial catch block, it isolates 
   "failure to raise anything" from "raised the wrong error type" inside the reporting logs.

## Downstream Fluid Interface Design
By returning the raw caught `BaseException` instance, this function acts as an ideal conduit for 
fluid assertions. The output can be piped directly into telemetry inspection blades (such as `assert_exception_fields`), 
enabling developers to validate deep error messages, codes, or dynamic hints raised from deep within the functional context.
"""