import math
import pytest
from typing import Any

# Importujeme přímo novou pomocnou funkci
from simplibs.exception.testing.asserts.fields._utils.compare_values import (
    compare_values,
)


@pytest.mark.parametrize(
    "test_val, exc_val",
    [
        # --- 1. IEEE 754 NaN Cases (The Primary Target) ---
        (float("nan"), float("nan")),
        (math.nan, math.nan),
        (float("nan"), math.nan),
        # --- 2. Standard Primitives ---
        (123, 123),
        (-45.67, -45.67),
        ("hello world", "hello world"),
        (True, True),
        (False, False),
        (None, None),
        # --- 3. Composite Data Structures ---
        ([1, 2, 3], [1, 2, 3]),
        ({"a": 1, "b": 2}, {"a": 1, "b": 2}),
        ((1, "test"), (1, "test")),
        ({1, 2, 3}, {1, 2, 3}),
    ],
)
def test_compare_values_passing_cases(test_val: Any, exc_val: Any) -> None:
    """Verify that identical primitives, complex objects, and float NaNs pass comparison without raising."""
    # Should complete silently without raising AssertionError
    compare_values(test_val, exc_val)


@pytest.mark.parametrize(
    "test_val, exc_val",
    [
        # --- 1. One NaN vs Non-NaN Float/Value ---
        (float("nan"), 123.45),
        (123.45, float("nan")),
        (float("nan"), "nan"),
        ("nan", float("nan")),
        # --- 2. Standard Value Mismatches ---
        (123, 456),
        ("foo", "bar"),
        (True, False),
        (10.0, 10.00001),
        (None, False),
        # --- 3. Mismatched Collections ---
        ([1, 2], [1, 2, 3]),
        ({"a": 1}, {"a": 2}),
    ],
)
def test_compare_values_failing_cases(test_val: Any, exc_val: Any) -> None:
    """Verify that unequal values or single-sided NaNs strictly trigger AssertionError."""
    with pytest.raises(AssertionError):
        compare_values(test_val, exc_val)


def test_compare_values_custom_objects() -> None:
    """Verify behavior with custom object instances."""

    class Dummy:
        def __init__(self, val: int):
            self.val = val

        def __eq__(self, other: Any) -> bool:
            return isinstance(other, Dummy) and self.val == other.val

    obj1 = Dummy(10)
    obj2 = Dummy(10)
    obj3 = Dummy(20)

    # Equal custom objects pass
    compare_values(obj1, obj2)

    # Non-equal custom objects fail
    with pytest.raises(AssertionError):
        compare_values(obj1, obj3)