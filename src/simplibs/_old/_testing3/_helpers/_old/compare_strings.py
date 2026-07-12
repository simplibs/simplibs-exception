from simplibs.sentinels import UnsetType


def compare_strings(
    test_value: str | tuple[str, ...] | None | UnsetType,
    exc_value: str | tuple[str, ...] | None | UnsetType,
    *,
    exact_match: bool,
) -> None:
    """Compare evaluation string metrics against target exception outputs.

    Provides multi-mode textual verification supporting absolute equality passes
    or dynamic substring inclusion lookups across normalized sequence structures.
    """

    # 1. Direct short-circuit for absolute equality evaluation
    if exact_match:
        assert test_value == exc_value
        return

    # 2. Substring inclusion fallback under fuzzy mode
    # Convert empty/None values to empty strings to guarantee safe joining
    raw_test = "" if test_value is None or isinstance(test_value, UnsetType) else test_value
    raw_exc = "" if exc_value is None or isinstance(exc_value, UnsetType) else exc_value

    # Normalize structural string sequences (tuples) into single text blocks
    normalized_test = " ".join(raw_test) if isinstance(raw_test, tuple) else raw_test
    normalized_exc = " ".join(raw_exc) if isinstance(raw_exc, tuple) else raw_exc

    # Enforce fuzzy validation gate
    assert normalized_test in normalized_exc


_DESIGN_NOTES = """
# compare_strings (Textual Inspector Helper)

## Purpose
An internal assertion engine specialized in verifying string and string-sequence attributes 
(such as error messages, problems, context arrays, or hints). It bridges the gap between 
strict literal data auditing and flexible, non-brittle diagnostics tracking.

## Operational Modalities

### 1. Absolute Equality Mode (`exact_match=True`)
The comparator triggers a direct equality verification gate (`assert test_value == exc_value`). 
This is critical for high-precision properties like `error_name`, custom metadata tokens, 
or strict validation flags where mutation is unacceptable.

### 2. Fuzzy Substring Mode (`exact_match=False`)
Optimized for testing dynamic outputs like long formatted messages, platform-specific backtraces, 
or generated advice. It converts `None` boundaries safely and flattens array/tuple sequences via 
whitespace aggregation (`" ".join(...)`). The evaluation passes if the expected string criteria is 
contained anywhere within the target exception readout (`assert test_value in exc_value`).
"""