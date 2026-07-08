from typing import Any


def print_intercepted_exception(
    exception: Any,
    *,
    prefix: str = "Intercepted exception",
    _log_mode: bool = False,
    _oneline: bool = False,
) -> str | None:
    """
    Renders information exclusively about a caught exception instance.
    Supporting standard multi-line, flat single-line, or machine-readable logfmt.
    """
    # 1. Type Guard: Only process active, caught instances of an Exception
    if not exception or not isinstance(exception, Exception):
        return None

    err_type = exception.__class__.__name__
    err_msg = str(exception).strip()

    # 2. LOG MODE: Emit only the machine-safe exception class type to prevent row breaks
    if _log_mode:
        return f"intercepted_exception={err_type!r}"

    # 3. ONELINE MODE: Inline the error type and flatten any multi-line message payloads
    if _oneline:
        if err_msg:
            # Flatten internal newlines inside third-party exception messages safely
            flat_msg = " ".join(err_msg.splitlines())
            return f"{prefix} ({err_type}): {flat_msg}"
        return f"{prefix} ({err_type})"

    # 4. STANDARD MODE: Human-friendly multiline breakdown of the cause
    if err_msg:
        return f"{prefix} ({err_type}):\n    {err_msg}"
    return f"{prefix} ({err_type})"


_DESIGN_NOTES = """
# print_intercepted_exception

## Purpose
Formats metadata regarding an underlying, caught root cause exception (e.g., an upstream error 
captured during an `except Exception as e` block) that triggered the current `SimpleException`.

## Execution Layout Routing

The function adapts dynamically based on operational control flags to enforce layout safety:

### 1. Standard Mode (Multi-line Structural View)
If the underlying exception contains a message payload, it is pushed down to a secondary, 
indented line under the prefix using `\\n    {err_msg}`. This creates a clean visual separation 
between primary `SimpleException` states and third-party error data:
```text
Intercepted exception (ValueError):
    invalid literal for int() with base 10: 'abc'

```

### 2. Oneline Mode (`_oneline=True`)

Explicitly guards horizontal row integrity. Instead of introducing a newline, it formats the error
into a flat horizontal stream. Furthermore, because third-party exceptions can contain chaotic multi-line
messages (e.g., raw SQL dumps), the engine passes `err_msg` through a high-performance `.splitlines()`
merging pass, collapsing vertical data into a single, space-separated string:

```text
Intercepted exception (ValueError): invalid literal for int() with base 10: 'abc'

```

### 3. Log Mode (`_log_mode=True`)

To safeguard row-based machine log parsers (Logstash, Datadog), log mode prunes the output down to
*only* the exception's formal class name wrapper, wrapped in safe `repr()` quotes via the `!r` flag.
The variable message payload is completely omitted to eliminate the risk of unsafe characters or
bloated structures corrupting telemetry streams:

```text
intercepted_exception='ValueError'

```

## Defensive Architecture (The Type Guard)

The framework applies a strict `isinstance(exception, Exception)` evaluation filter. If a developer
specifies a static fallback class or a blueprint type rather than an active runtime failure instance
(e.g., `exception = ValueError`), the printer silently short-circuits and returns `None`, shielding
downstream renderers from uninstantiated type failures.

## Usage Matrix

```python
# Rich multi-line human-readable panel display
print_intercepted_exception(data.exception)

# Flat horizontal grep-friendly terminal row segment
print_intercepted_exception(data.exception, _oneline=True)

# Machine telemetry log token emitting class type signature
print_intercepted_exception(data.exception, _log_mode=True)

```

"""