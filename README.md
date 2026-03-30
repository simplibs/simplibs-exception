# simplibs-exception

> An exception that tries to be a friend. A structured exception with diagnostic
> output, allowing you to describe the cause of an error, the circumstances of
> its occurrence, and the path to a fix. Fully compatible with standard Python
> exceptions — it simply extends them with more possibilities.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Licence](https://img.shields.io/badge/licence-MIT-green)
![PyPI](https://img.shields.io/pypi/v/simplibs-exception)
```
═════════════════════════════════════════════════════════════════
⚠️ VALIDATION ERROR: parameter age
═════════════════════════════════════════════════════════════════
Expected:  a positive integer
Got:       -5 (int)
Problem:   value is negative
File info: File: main.py | Line: 42 | Path: ... | Function: validate
─────────────────────────────────────────────────────────────────
🔧 How to fix:
     • Provide a value greater than 0.
     • Use the int type.
═════════════════════════════════════════════════════════════════
```

---

## Contents

- [Installation](#installation)
- [Quick start](#quick-start)
- [Parameters](#parameters)
- [Custom exceptions](#custom-exceptions)
- [Output modes](#output-modes)
- [Global settings](#global-settings)
- [Custom mode](#custom-mode)
- [Serialisation](#serialisation)
- [Utils](#utils)
- [About the simplibs ecosystem](#about-the-simplibs-ecosystem)

---

## Installation
```bash
pip install simplibs-exception
```
```python
from simplibs.exception import SimpleException
```

> Note: This library automatically installs `simplibs-sentinels` as a core dependency.

---

## Quick start

Python exceptions are a powerful tool — but their default output is terse.
We see *where* the error occurred, but not *what* exactly failed, *why* it
failed, or *how to fix it*. `SimpleException` changes that — on one hand it
works exactly like a regular Python exception, but it also gives you the option
of richer content for detailed diagnostics and actionable remediation. No
parameter is required, so you can start with nothing and add detail as needed.

### Empty call — location only

Useful during rapid development when you just want to know *where* an exception
occurred without worrying about its content yet. Mark the spot and come back
to it later:
```python
raise SimpleException()
# ═══════════════════════════════════════════════════════════════════
# ⚠️ ERROR: File: main.py | Line: 42 | Path: ... | Function: validate
# ═══════════════════════════════════════════════════════════════════
```

### Message only — like a classic exception

If you don't need structure — or just want to jot down an initial thought and
fill in the details later — `SimpleException` behaves exactly like `Exception`,
but with a nicer default output:
```python
raise SimpleException("Database connection failed")
# ═══════════════════════════════════════════════════════════════════
# ⚠️ ERROR: Database connection failed
# File: main.py | Line: 15 | Path: ... | Function: connect
# ═══════════════════════════════════════════════════════════════════
```

### Full structured use

This is where the real power of the library shows — the exception communicates,
it doesn't just announce. You have full freedom over what you report and which
parameters you use. For the exception to be truly useful, it's worth filling
in the core parameters and especially `how_to_fix` — but none of it is
required:
```python
raise SimpleException(
    value_label = "parameter age",
    expected    = "a positive integer",
    value       = age,
    problem     = "value is negative",
    how_to_fix  = "Provide a value greater than 0.",
)
# ═══════════════════════════════════════════════════════════════════
# ⚠️ ERROR: parameter age
# ═══════════════════════════════════════════════════════════════════
# Expected:  a positive integer
# Got:       -5 (int)
# Problem:   value is negative
# File info: File: main.py | Line: 42 | Path: ... | Function: validate
# ───────────────────────────────────────────────────────────────────
# 🔧 How to fix:
#      • Provide a value greater than 0.
# ═══════════════════════════════════════════════════════════════════
```

---

## Parameters

An overview of all parameters available when raising the exception. All are
optional — the exception works without any of them (see above).

| Parameter       | Type                      | Description                                                      |
|-----------------|---------------------------|------------------------------------------------------------------|
| `message`       | `str`                     | Free-form message — an alternative to the structured fields      |
| `value`         | `object`                  | The value that caused the exception                              |
| `value_label`   | `str`                     | Human-readable label for the value (e.g. `"parameter age"`)     |
| `expected`      | `str`                     | What was expected                                                |
| `problem`       | `str`                     | What is wrong                                                    |
| `context`       | `str`                     | Additional context — only include if it adds meaningful info     |
| `how_to_fix`    | `str \| tuple[str, ...]`  | Tips on how to fix the error — one or more                       |
| `error_name`    | `str`                     | Error name in the output (default: `"ERROR"`)                    |
| `exception`     | `type[Exception]`         | Exception class dynamically added to the instance ancestors      |
| `get_location`  | `bool \| int`             | Enable/disable or set stack depth for location (default: `True`) |
| `skip_locations`| `tuple[str, ...]`         | File path patterns to skip when resolving the call location      |
| `oneline`       | `bool`                    | Single-line output for this specific call                        |

### More about the `exception` parameter

The `exception` parameter allows you to pass a specific Python exception into
the ancestors of the instance. The raised exception will then be catchable as
that specific type — without requiring static inheritance:
```python
from simplibs.exception import SimpleException

# As a class — the exception behaves as a ValueError
raise SimpleException(exception=ValueError, problem="negative value")

# From an except block — pass the instance directly
try:
    int("abc")
except ValueError as e:
    raise SimpleException(exception=e, problem="could not convert to int")

# Verify catchability
try:
    raise SimpleException(exception=ValueError)
except ValueError:
    print("caught as ValueError ✓")
```

---

## Custom exceptions

`SimpleException` can serve as the base for your own exception classes — for
example for a specific validation domain. You define the shared default
interface once, so that callers don't have to repeat the same parameters every
time:
```python
from simplibs.exception import SimpleException

class AgeError(SimpleException):
    error_name = "VALIDATION ERROR"
    expected   = "a positive integer"
    how_to_fix = (
        "Provide a value greater than 0.",
        "Use the int type.",
    )

# At the call site, only the specific values are needed —
# error_name, expected and how_to_fix are inherited from the class
raise AgeError(value=age, value_label="parameter age")
# ═══════════════════════════════════════════════════════════════════
# ⚠️ VALIDATION ERROR: parameter age
# ═══════════════════════════════════════════════════════════════════
# Expected:  a positive integer
# Got:       -5 (int)
# File info: File: main.py | Line: 8 | Path: ... | Function: validate_age
# ───────────────────────────────────────────────────────────────────
# 🔧 How to fix:
#      • Provide a value greater than 0.
#      • Use the int type.
# ═══════════════════════════════════════════════════════════════════

# Class-level attributes can always be overridden at the call site —
# the class definition is a default state, not a constraint
raise AgeError(
    value       = age,
    value_label = "user age",
    expected    = "a number between 18 and 120",  # overrides the class default
)
```

The library automatically validates every subclass at definition time —
checking for typos and incorrect attribute types. The error surfaces
immediately on import, not somewhere at runtime:
```python
class BadError(SimpleException):
    expekted = "a positive integer"  # typo in the attribute name
# → INTERNAL ERROR on import — the typo is caught immediately
```

---

## Output modes

The library provides four output modes. The default is `PRETTY` — a structured
output framed with separator lines. The mode can be changed globally via
settings or overridden for a single call using `oneline=True`.

| Mode      | Description                                                           |
|-----------|-----------------------------------------------------------------------|
| `PRETTY`  | Structured output with double separator lines — the default mode      |
| `SIMPLE`  | Identical content to PRETTY but without the decorative lines          |
| `ONELINE` | Everything on one line separated by `\|` — suited for quick debugging |
| `LOG`     | `key=value` format for log parsers (Datadog, Splunk, ...)             |

### PRETTY (default)
```
═════════════════════════════════════════════════════════════════
⚠️ VALIDATION ERROR: parameter age
═════════════════════════════════════════════════════════════════
Expected:  a positive integer
Got:       -5 (int)
Problem:   value is negative
File info: File: main.py | Line: 42 | Path: ... | Function: validate
─────────────────────────────────────────────────────────────────
🔧 How to fix:
     • Provide a value greater than 0.
═════════════════════════════════════════════════════════════════
```

### SIMPLE
```
⚠️ VALIDATION ERROR: parameter age
Expected:  a positive integer
Got:       -5 (int)
Problem:   value is negative
File info: File: main.py | Line: 42 | Path: ... | Function: validate
🔧 How to fix:
     • Provide a value greater than 0.
```

### ONELINE
```
⚠️ VALIDATION ERROR | parameter age | Expected: a positive integer | Got: -5 (int) | Problem: value is negative | File: main.py | Line: 42
```

### LOG
```
error=VALIDATION ERROR value_label='parameter age' expected='a positive integer' value='-5 (int)' problem='value is negative' file='main.py' line=42
```

---

## Global settings

`SimpleExceptionSettings` is the central configuration for the entire
ecosystem. Changes apply to all exceptions in the project — no need to
override anything on individual classes:
```python
from simplibs.exception import SimpleExceptionSettings, LOG

# Change the output mode — for example in production
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = LOG

# Disable location reporting
SimpleExceptionSettings.DEFAULT_GET_LOCATION = False

# Skip your own files when resolving the call location
# — useful if you have helper validation functions you don't want to see in output
SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST = ("my_validators.py",)

# Reset everything to factory defaults
SimpleExceptionSettings.reset()
```

Settings are protected by internal validation — if you provide an invalid
value, you get a clear error message instead of a mysterious crash:
```python
SimpleExceptionSettings.DEFAULT_GET_LOCATION = "enabled"
```
```
═════════════════════════════════════════════════════════════════
⚠️ SETTINGS ERROR: DEFAULT_GET_LOCATION
═════════════════════════════════════════════════════════════════
Expected:  int or bool (e.g. True, False, 1, 2)
Got:       "enabled" (str)
Problem:   value is neither an int nor a bool
─────────────────────────────────────────────────────────────────
🔧 How to fix:
     • Pass True or False to enable or disable location reporting.
     • Pass an int to set the stack depth (e.g. 1, 2).
═════════════════════════════════════════════════════════════════
```

---

## Custom mode

If none of the built-in modes suits your needs, you can create your own.
Simply inherit from `ModeBase` and implement one method:
```python
from simplibs.exception import ModeBase, SimpleExceptionSettings
from simplibs.exception.core import SimpleExceptionData

class SlackMode(ModeBase):
    """Output formatted for Slack notifications."""

    def _full_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        parts = [f":warning: *{data.error_name}*"]
        if data.value_label:
            parts.append(f"*Value:* {data.value_label}")
        if data.problem:
            parts.append(f"*Problem:* {data.problem}")
        if data.how_to_fix:
            parts.append("*How to fix:*\n" + "\n".join(f"• {tip}" for tip in data.how_to_fix))
        return "\n".join(parts)

SLACK_MODE = SlackMode()
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = SLACK_MODE
```

When creating a custom mode, you can define up to three output methods.
Only `_full_outcome` is required — `_empty_outcome` and `_message_outcome`
have sensible defaults and can be overridden only when needed.

All fields available via `data` are listed in the [Parameters](#parameters) section.
In addition, `ModeBase` provides three helper methods for formatting:

| Method                            | Description                                               |
|-----------------------------------|-----------------------------------------------------------|
| `_print_intro_line(data)`         | Builds the opening line with `error_name` and `value_label` |
| `_print_value_with_type(data)`    | Value with type — e.g. `"hello" (str)`                    |
| `_print_caller_info(caller_info)` | Formats the location as a string or dictionary            |

---

## Serialisation

Every `SimpleException` instance can serialise its state — useful for logging,
transport, or storing error reports:
```python
from simplibs.exception import SimpleException

e = SimpleException(
    value_label = "parameter age",
    expected    = "a positive integer",
    value       = -5,
    problem     = "value is negative",
)

e.to_dict()        # public attributes as a dictionary — UNSET values omitted
e.to_json()        # JSON string — same data, suited for transport
e.to_debug_dict()  # complete state including internal values — for debugging
```
```python
e.to_dict()
# {
#     "error_name":  "ERROR",
#     "value":       -5,
#     "value_label": "parameter age",
#     "expected":    "a positive integer",
#     "problem":     "value is negative",
# }
```

---

## Utils

Alongside the exception itself, the library provides two utility tools that
are also available independently.

### bool_or_exception

A shortcut for the pattern where a function either returns `False` or raises
a `SimpleException`. Eliminates repetitive conditional code in places where
a `return_bool` parameter exists — a flag that controls whether to return
`False` on failure instead of raising:
```python
from simplibs.exception import bool_or_exception

def validate_age(age: int, return_bool: bool = False) -> bool:
    if age <= 0:
        return bool_or_exception(
            return_bool,
            value_label = "parameter age",
            expected    = "a positive integer",
            value       = age,
        )
    return True
```

### extract_caller_info

A diagnostic function that walks the call stack and returns information about
the first relevant frame — file, line number, function name, and full path.
The function never raises an exception — it returns `None` on failure. It is
completely independent of the rest of the library and can be used anywhere:
```python
from simplibs.exception import extract_caller_info

info = extract_caller_info()
# {
#     "file":      "main.py",
#     "full_path": "/projects/app/main.py",
#     "line":      42,
#     "function":  "validate",
# }
```

---

## About the simplibs ecosystem

`simplibs-exception` is the foundation of the **simplibs** ecosystem — it gives
the ecosystem a voice, helping it communicate with the user in a clear and
human way: not just reporting what went wrong, but pointing towards a fix.
The name *simplibs* is short for *simple libraries*.

This library builds on one other simplibs package:

- **`simplibs-sentinels`** — sentinel values shared across the ecosystem.
  `UNSET` is used throughout `simplibs-exception` to distinguish between
  a parameter that was not provided and one explicitly set to `None`:
```python
from simplibs.sentinels import UNSET
```

All libraries in the simplibs ecosystem share a common philosophy:

**Dyslexia-friendly** — minimise mental load. Atomise code into self-contained
units, name files after the logic they contain, write explanations that describe
*why* — not just *what*.

**Programmer's zen** — nothing should be missing and nothing should be
superfluous. The journey is the destination: code should be fully understood;
better to go slowly and correctly than quickly and with mistakes. The
crystallisation approach — not perfection on the first try, but gradual
refinement towards it.

**Defensive style** — anticipate all possible failure modes so that only safe
paths remain. Never raise unexpected errors; degrade gracefully.

**Minimalism** — find the path to the goal in as few steps as possible, but
leave nothing out. Each file has one responsibility.

**Code as craft** — code should be pleasant to look at and evoke a sense of
harmony. Treat code as a small work of art — like a carpenter carving a
sculpture. Optimise for the user: everything should make sense without having
to study the documentation at length.

These are aspirations — a sense of direction. And that is exactly what the
note about the journey becoming the destination is all about. 🙂

---

*The library is covered by tests across all modules — unit tests and
integration tests alike. Tests are part of the repository and serve
as living documentation of the expected behaviour.*