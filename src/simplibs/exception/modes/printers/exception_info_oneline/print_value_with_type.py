from typing import Any
from simplibs.sentinels import UNSET


def print_value_with_type(
    value: Any,
    max_length: int | None = None,
    *,
    prefix: str = "Got:       ",
    _log_mode: bool = False
) -> str | None:
    """
    Renders the runtime value along with its data type wrapper.
    Handles data truncation gracefully based on global or local length constraints.
    """
    # 1. Short-circuit if the value was never supplied
    if value is UNSET:
        return None

    # 2. Extract the safe evaluation representation
    repr_str = repr(value)

    # 3. Fallback to global application configuration if local override is omitted
    if max_length is None:
        from ....SimpleExceptionSettings import SimpleExceptionSettings as S
        max_length = S.VALUE_TRUNCATION_LENGTH

    # 4. Truncation engine execution
    is_truncated = len(repr_str) > max_length
    if is_truncated:
        truncated_chars = len(repr_str) - max_length
        repr_str = (
            repr_str[:max_length] +
            f"... [truncated, {truncated_chars} chars]"
        )

    # 5. LOG MODE: Build safe key-value attributes for indexers
    if _log_mode:
        # If truncated, the string now contains plain text modifiers and spaces.
        # We must re-wrap with !r to guarantee valid token encapsulation.
        # Otherwise, the clean repr_str already possesses structural quotes.
        final_val = repr_str if not is_truncated else f"{repr_str!r}"
        return f"value={final_val} type={type(value).__name__}"

    # 6. STANDARD MODE: Human-focused presentation string containing explicit type markers
    return f"{prefix}{repr_str} ({type(value).__name__})"


_DESIGN_NOTES = """
# print_value_with_type

## Purpose
Inspects and prints the actual dynamic value received at runtime that triggered 
the exception boundary, decorated with its primitive or complex native Python class type name.

## Guarding Against Infinite Payload Bloat (Truncation)
Exceptions often intercept large payloads (e.g., massive JSON strings, database query buffers, 
or binary dumps). Printing these fully would flood stdout or log infrastructure. 
The function calculates character boundaries and truncates excessive data, appending a 
clear structural footprint marker showing exactly how many characters were sliced away:
`"very_long_string..."... [truncated, 1500 chars]`.

## Log Mode Row Safety & Conditional Escaping
When compiling logs (`_log_mode=True`), preserving format boundary structures is paramount. 
The function uses a smart conditional format strategy:
- **No Truncation**: The output of `repr(value)` is natively isolated with its own valid 
  quotes (e.g., `'my_value'`). It is safe to emit as-is.
- **Truncated Payload**: Because the truncation logic injects free-form bracket text 
  `... [truncated, X chars]`, the string now contains raw spaces. Emitting this raw would 
  break space-delimited log collectors. Re-wrapping with `!r` guarantees the modified 
  string stays securely grouped within a single quoted field payload token.

## Usage
Interposed as a fundamental observation layer inside rendering matrices:
```python
lines = [
    # ...
    print_expected(data.expected),
    print_value_with_type(data.value),
    # ...
]
"""


_DESIGN_NOTES = """
# PrintValueWithTypeMixin

## Purpose
Builds a readable representation of the inspected value, including its type 
and handling potential truncation of extremely long strings.

## Truncation Logic
To prevent the exception message from being overwhelmed by large data objects 
(like massive dictionaries or long strings), the mixin automatically truncates 
the `repr()` of the value.
- **Default limit**: Controlled by `SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH`.
- **Manual override**: Can be specified via the `max_length` argument.
- **Feedback**: If truncated, it appends a notice with the count of hidden characters.

## Output Examples
```
# Standard:
Got: "hello" (str)

# Truncated:
Got: "very long str..." [truncated, 450 chars] (str)

# If value is UNSET:
None
```

## Integration
Like all output mixins, this one follows the unified signature: it accepts 
the `SimpleExceptionData` object. This ensures consistency across all modes 
(PRETTY, LOG, etc.) and keeps the rendering workflow predictable.

## Notes
- Returns `None` if `data.value` is `UNSET`. Callers typically use `if line: ...` 
  to skip rendering this line entirely.
- It uses `repr()` instead of `str()` to ensure that the representation 
  is unambiguous (e.g., distinguishing between `'5'` and `5`).
"""