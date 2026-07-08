def print_expected(
    expected: str | None,
    *,
    prefix: str = "Expected:  ",
    _log_mode: bool = False
) -> str | None:
    """
    Renders the descriptive expectation threshold (what the system actually anticipated).
    """
    if not expected:
        return None

    # 1. LOG MODE: Secure string representation for centralized logging
    if _log_mode:
        return f"expected={expected!r}"

    # 2. STANDARD MODE: Human-friendly literal rendering with a fixed prefix margin
    return prefix + expected


_DESIGN_NOTES = """
# print_expected

## Purpose
Renders the strict specification constraint or condition (`expected`) that the 
runtime environment was anticipating before the violation occurred.

## Visual Symmetry
In pair with `print_value_with_type` (the "Got:" line), `print_expected` helps build 
a classic assertion-style comparison layout inside the exception body. It utilizes 
a precision-padded 11-character `prefix` (`"Expected:  "`) to ensure that both the 
anticipated condition and the actual faulty payload line up perfectly on the left margin, 
making visual diffing effortless for a human operator.

## Log Mode Row Safety via Repr (!r)
When `_log_mode=True`, the string is sanitized using the `!r` formatting flag. 
Since criteria parameters might include code symbols, types, or raw validation rules 
containing whitespace, raw quotes, or commas, `repr()` encapsulation guarantees 
the field token maps cleanly as a single entity in space-delimited text log parsers.

## Usage
Placed immediately prior to the runtime value observer token inside the layout matrix:
```python
lines = [
    # ...
    print_message(data.message),
    print_expected(data.expected),
    print_value_with_type(data.value),
    # ...
]
"""