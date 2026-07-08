def print_intro(
    error_name: str,
    label: str | None,
    *,
    prefix: str = "⚠️ ",
    _log_mode: bool = False
) -> str:
    """
    Renders the primary error header, combining the error name and an optional label.
    Adapts dynamically between machine-readable log format and human-friendly terminal layouts.

    Output Formats:
        Standard Mode:
            Structure: <PREFIX><ERROR_NAME>[: <LABEL>]
            Examples:
                       ⚠️ VALUE_ERROR
                       ⚠️ VALUE_ERROR: Invalid email format

        Log Mode (_log_mode=True):
            Structure: error='<ERROR_NAME>'[ label='<LABEL>']
            Examples:
                       error='VALUE_ERROR'
                       error='VALUE_ERROR' label='Invalid email format'
    """
    # 1. LOG MODE: Structured key-value formatting for log parsers
    if _log_mode:
        if label:
            return f"error={error_name!r} label={label!r}"
        return f"error={error_name!r}"

    # 2. STANDARD MODE: Human-readable presentation header with visual emoji prefix
    if label:
        return f"{prefix}{error_name}: {label}"
    return f"{prefix}{error_name}"


_DESIGN_NOTES = """
# print_intro

## Purpose
Renders the foundational identification line (the "header") of the exception. 
It cleanly pairs the strict `error_name` identifier with an optional, 
context-specific human `label`.

## Dual-Mode Architecture
This printer behaves fundamentally differently based on the operational mode:
1. **Standard/Pretty Mode**: Optimized for high-impact visual terminal feedback. 
   It introduces a prominent warning emoji (`prefix`) and strings the components 
   together naturally (e.g., `⚠️ VALIDATION_ERROR: Invalid Email Format`).
2. **Log Mode**: Strips away all decorative elements like emojis and prefixes 
   to maintain clean, machine-parsable logging fields. It renders a normalized 
   key-value output (e.g., `error='VALIDATION_ERROR' label='Invalid Email Format'`).

## Use of Explicit Repr (!r) in Logs
When processing log emission, if a `label` is provided, it is sanitized using 
the `!r` formatting flag. Because user-supplied labels might contain spaces, 
quotes, or unexpected characters, wrapping them in their native string representation 
prevents key-value parser breakage in log analytics stacks (e.g., Elasticsearch/Kibana).

## Usage
Invoked as the leading metadata field in both `PrettyMessage` and log rendering routines:
```python
lines = [
    DOUBLE_LINE,
    print_intro(data.error_name, data.label),
    # ...
]
"""