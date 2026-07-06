def print_message(
    message: str | None,
    *,
    prefix: str = "Message:   ",
    _log_mode: bool = False
) -> str | None:
    """
    Renders the primary human-readable message string explaining the exception context.

    If the input value is empty or omitted, the function gracefully returns None.

    Output Formats:
        Standard Mode:
            Structure: <PREFIX><MESSAGE>
            Example:   Message:   The requested user ID was not found in the database.

        Log Mode (_log_mode=True):
            Structure: message='<MESSAGE>'
            Example:   message='The requested user ID was not found in the database.'
    """
    if not message:
        return None

    # 1. LOG MODE: Secure string representation for log aggregators
    if _log_mode:
        return f"message={message!r}"

    # 2. STANDARD MODE: Human-friendly literal message rendering with a fixed prefix margin
    return prefix + message


_DESIGN_NOTES = """
# print_message

## Purpose
Renders the foundational, core text sentence (`message`) that describes the high-level 
nature of what failed at runtime.

## Layout Simplicity
Unlike `print_problem` or `print_context` which manage complex multi-line string tuples 
using `EMPTY_PREFIX` alignment columns, `print_message` processes a single, flat string. 
It aligns perfectly with the standard fixed-width layout margin strategy by prepending 
the standard 11-character `prefix` (`"Message:   "`), maintaining visual uniformity 
across the entire rendering panel.

## Log Mode Row Safety via Repr (!r)
When `_log_mode=True`, the core message text is safely encapsulated using the `!r` formatting 
flag. Because user-defined error messages frequently contain spaces, quotes, punctuation, 
or dynamic runtime values, string escaping via `repr()` is critical to ensure that row-based 
log parsers read the entire message token as a single bounded field value.

## Usage
Acts as the very first core body item inside the formatting structure:
```python
lines = [
    # ...
    DOUBLE_LINE if has_details else None,
    print_message(data.message),
    print_expected(data.expected),
    # ...
]
"""
