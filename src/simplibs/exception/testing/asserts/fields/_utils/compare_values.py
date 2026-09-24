import math
from typing import Any


def compare_values(
    test_value: Any,
    exc_value: Any,
) -> None:
    """Compare target exception value attributes with IEEE 754 NaN safety.

    Provides strict equality assertions between expected test parameters and
    retrieved exception attributes, handling edge cases where standard Python
    equality breaks (specifically float NaN comparisons where float('nan') != float('nan')).

    Args:
        test_value: The expected value or payload to verify.
        exc_value: The actual value retrieved from the exception instance.

    Raises:
        AssertionError: If test_value does not equal exc_value and they are not both NaN.
    """
    # 1. IEEE 754 NaN Safety Gate: Ensure float('nan') == float('nan') evaluates as valid
    if (
        isinstance(test_value, float)
        and isinstance(exc_value, float)
        and math.isnan(test_value)
        and math.isnan(exc_value)
    ):
        return

    # 2. Standard Value Equality Evaluation
    assert test_value == exc_value


_DESIGN_NOTES = """
# compare_values (Value Inspector Helper)

## Purpose
An internal assertion engine specialized in verifying generic data values and payloads 
captured within exception telemetry (such as `exc.value`). It provides exact equality 
verification while resolving edge-case failures inherent to Python's handling of special numeric types.

## The IEEE 754 NaN Neutralization Strategy
In standard Python and IEEE 754 specs, `float("nan") == float("nan")` evaluates strictly to `False`. 
When testing valid/invalid contract boundary batteries with NaN values, standard `assert test_value == exc_value` 
fails even when the exception correctly captured the exact input object.

This engine introduces an explicit type and state check (`isinstance` + `math.isnan`). If both sides 
are confirmed NaN floats, the comparison passes safely before reaching the standard equality gate.

## Operational Scope
Unlike `compare_strings`, this engine does not perform normalization, substring matching, or prefix 
evaluations. It enforces exact identity/equality semantics across standard data types (ints, floats, 
objects, collections, custom types) with NaN immunity.
"""