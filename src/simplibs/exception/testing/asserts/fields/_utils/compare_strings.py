from typing import Any
# Inners
from .normalize_value import normalize_value


def compare_strings(
    test_value: Any,
    exc_value: Any,
    *,
    exact_match: bool = False,
    startswith: bool = False,
) -> None:
    """Compare evaluation string metrics against target exception outputs.

    Provides multi-mode textual verification supporting absolute equality passes
    or dynamic substring inclusion lookups across normalized sequence structures.

    Args:
        test_value: The expected value or criteria to verify.
        exc_value: The actual value retrieved from the exception object.
        exact_match: If True, triggers strict equality evaluation.
        startswith: If True, validates the prefix of the exception readout.

    Raises:
        AssertionError: If the comparison criteria are not met.
    """

    # Normalize inputs via the dedicated flattening utility
    normalized_test = normalize_value(test_value)
    normalized_exc = normalize_value(exc_value)

    # 1. Absolute Equality Mode (Highest Priority)
    if exact_match:
        assert normalized_test == normalized_exc
        return

    # 2. Prefix Mode (Secondary Priority)
    if startswith:
        assert normalized_exc.startswith(normalized_test)
        return

    # 3. Fuzzy Substring Mode (Default)
    assert normalized_test in normalized_exc


_DESIGN_NOTES = """
# compare_strings (Textual Inspector Helper)

## Purpose
An internal assertion engine specialized in verifying string and string-sequence attributes 
(such as error messages, problems, context arrays, or hints). It bridges the gap between 
strict literal data auditing and flexible, non-brittle diagnostics tracking.

## Operational Modalities (Evaluation Hierarchy)

### 1. Absolute Equality Mode (`exact_match=True`)
Triggers a direct equality verification gate (`assert test_value == exc_value`). 
Critical for high-precision properties like `error_name`, custom metadata tokens, 
or strict validation flags where mutation is unacceptable.

### 2. Prefix Validation Mode (`startswith=True`)
Validates that the target exception output begins with the expected test criteria.
Ideal for verifying dynamic messages where the specific error header is known, 
but the trailing diagnostics (e.g., stack traces or runtime metadata) may vary.

### 3. Fuzzy Substring Mode (`default`)
Optimized for testing dynamic outputs like long formatted messages or generated advice. 
The evaluation passes if the expected string criteria is contained anywhere within 
the target exception readout (`assert test_value in exc_value`).

## Architectural Integration
This engine utilizes `normalize_value` as a data-sanitization layer, ensuring that 
all comparisons are performed against flattened, deterministic string buffers. This 
abstraction allows the engine to remain agnostic to the underlying input types 
(tuples, None, Unset tokens) while maintaining high-speed execution profiles.
"""