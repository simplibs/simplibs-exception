# simplibs-exception

> **An exception that tries to be a friend.**
>
> A structured Python exception that doesn't just crash—it explains what went wrong, 
> why it happened, and how to fix it. Beautiful output. Zero filler.

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
File info: File: main.py | Line: 42 | Function: validate
File path: /path/to/project/main.py
─────────────────────────────────────────────────────────────────
🔧 How to fix:
     • Provide a value greater than 0.
     • Use the int type.
═════════════════════════════════════════════════════════════════
```

---

## Table of Contents

- [Why This Library?](#why-this-library)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Parameters](#core-parameters)
- [Custom Exceptions](#custom-exceptions)
- [Dynamic Exception Types](#dynamic-exception-types)
- [Output Modes](#output-modes)
- [Utilities](#utilities)
- [Serialization](#serialization)
- [Global Settings](#global-settings)
- [Advanced: Stack Filtering for Library Development](#advanced-stack-filtering-for-library-development)
- [Custom Output Modes](#custom-output-modes)
- [About simplibs](#about-simplibs)
- [Reference](#reference)
- [License](#license)

---

## Why This Library?

Standard Python exceptions tell you *where* code broke (line number), but they're terrible at telling you *what* was in your variables or *how to fix it*. You end up jamming everything into f-strings and hoping it makes sense.

`simplibs-exception` changes that. Instead of generic crashes, you get **diagnostic reports**: structured context about the problem, what you expected vs. got, and actionable next steps. Whether you're building a CLI, API, or validation pipeline, your exceptions finally help instead of hurt.

---

## Installation

```bash
pip install simplibs-exception
```

That's it. The library includes `simplibs-sentinels` automatically.

---

## Quick Start

You can start empty and add richness as needed. **No parameters are required.**

### Level 1: The Marker
Just mark the spot when you're unsure what to do.

```python
from simplibs.exception import SimpleException

raise SimpleException()
# ⚠️ ERROR: File: main.py | Line: 42 | Function: validate
```

### Level 2: The Message
Use it like a normal exception but with better formatting.

```python
raise SimpleException("Database connection timed out after 30s")
```

### Level 3: The Full Diagnostic
This is where the magic happens. Give your exception *context*.

```python
raise SimpleException(
    label = "parameter age",
    expected    = "a positive integer",
    value       = age,
    problem     = "value is negative",
    how_to_fix  = "Provide a value greater than 0."
)
```

---

## Core Parameters

All optional. Mix and match as needed.

| Parameter | Type | What It Does |
| :--- | :--- | :--- |
| `message` | `str` | Free-form message — use instead of structured fields if you prefer |
| `label` | `str` | Human label for the thing that broke (e.g., `"parameter age"`) |
| `value` | `any` | The actual value that caused the problem (auto-truncated if huge) |
| `expected` | `str` | What you wanted to see |
| `problem` | `str` | What went wrong |
| `context` | `str` | Extra info (only include if it matters) |
| `how_to_fix` | `str` or `tuple[str, ...]` | One or more hints on how to solve it |
| `error_name` | `str` | Custom error label (default: `"ERROR"`) |

### Bonus Parameters

| Parameter | Type | What It Does |
| :--- | :--- | :--- |
| `exception` | `Exception class or instance` | Make the exception catchable as a specific type |
| `get_location` | `bool` or `int` | Enable/disable file location tracking (or set stack depth) |
| `skip_locations` | `tuple[str, ...]` | File patterns to ignore when finding the error location |

---

## Custom Exceptions

Stop repeating yourself. Define once, use everywhere.

```python
class AgeValidationError(SimpleException):
    error_name = "VALIDATION ERROR"
    expected   = "a positive integer"
    how_to_fix = (
        "Provide a value greater than 0.",
        "Use the int type.",
    )

# Now just pass the specifics
raise AgeValidationError(value=age, label="parameter age")
```

The library validates subclass definitions at import time, catching typos immediately instead of crashing at runtime. 🎯

---

## Dynamic Exception Types

Sometimes you need to wrap a caught exception with more context, preserving the original error information without losing type information.

### Basic Usage: Static Exception Class

When you know the exception type upfront, pass the class:

```python
raise SimpleException(exception=ValueError, problem="negative value")
```

Now the exception is catchable as `ValueError`:

```python
try:
    raise SimpleException(exception=ValueError)
except ValueError:
    print("Caught! ✓")
```

### Advanced Usage: Instance from an Except Block

When you catch a real exception, pass the instance directly. The library extracts the exception type **and preserves the original message**:

```python
import json
from simplibs.exception import SimpleException

def load_json(raw_data):
    try:
        return json.loads(raw_data)
    except ValueError as e:
        raise SimpleException(
            exception=e,  # Pass the caught instance
            value=raw_data,
            label="JSON input",
            expected="valid JSON",
            problem="JSON parsing failed",
            how_to_fix="Check for syntax errors: mismatched quotes, trailing commas, etc."
        )
```

The original exception message is displayed **below the main exception frame** as "Intercepted exception":

```
═════════════════════════════════════════════════════════════════
⚠️ ERROR: JSON input
═════════════════════════════════════════════════════════════════
Expected:  valid JSON
Got:       '{"broken": }' (str)
Problem:   JSON parsing failed
File info: File: parser.py | Line: 15 | Function: load_json
File path: /path/to/project/parser.py
─────────────────────────────────────────────────────────────────
🔧 How to fix:
     • Check for syntax errors: mismatched quotes, trailing commas, etc.
═════════════════════════════════════════════════════════════════
Intercepted exception (ValueError):
    Expecting value: line 1 column 1 (char 0)
```

The exception is still catchable as `ValueError`:

```python
try:
    load_json('{"broken": }')
except ValueError:
    print("Caught as ValueError! ✓")
```

---

## Output Modes

Your exception can speak different languages depending on context.

### PRETTY (Default)
Beautiful framed output for development. This is what you see above.

### SIMPLE
Same info, no decorative borders. Good for plain-text logs.

```
⚠️ VALIDATION ERROR: parameter age
Expected:  a positive integer
Got:       -5 (int)
Problem:   value is negative
🔧 How to fix:
     • Provide a value greater than 0.
```

### ONELINE
Everything compressed to one line. Perfect for tight logs.

```
⚠️ VALIDATION ERROR | parameter age | Expected: a positive integer | Got: -5 (int)
```

### LOG
Machine-readable `key=value` format. Send this to Datadog, Splunk, or ELK.

```
error=VALIDATION ERROR label='parameter age' expected='a positive integer' value='-5 (int)' problem='value is negative'
```

### Switch Modes

```python
from simplibs.exception import SimpleExceptionSettings, LOG

# Change globally
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = LOG

# Or just for one exception
raise SimpleException(message="Oops", oneline=True)
```

---

## Utilities

### `bool_or_exception()`

Tired of writing `if not valid: raise ...`? Use this shortcut.

```python
from simplibs.exception import bool_or_exception

def validate_email(email, return_bool=False):
    if "@" not in email:
        return bool_or_exception(
            return_bool,
            value=email,
            problem="missing @ symbol"
        )
    return True

# Use it both ways
is_valid = validate_email("user@example.com", return_bool=True)  # Returns True
validate_email("invalid")  # Raises SimpleException
```

### `raise_with_location_offset()`

Sometimes you need to raise an exception that's already been instantiated, but with a shifted stack trace. This function wraps that pattern into a single call.

```python
from simplibs.exception import raise_with_location_offset

def my_parser(data):
    try:
        process(data)
    except ValueError as e:
        # Re-raise it, but make it look like the error came from the caller
        raise_with_location_offset(e, offset=1)
```

The function uses duck typing — if your exception has a `with_location_offset` method (like `SimpleException` does), it's applied. Otherwise, the exception is re-raised as-is. This keeps the tool flexible and avoids circular imports.

**Design note:** We don't import `SimpleException` directly. Instead, we check for the method at runtime with `hasattr()`. This makes the tool work with any exception class that implements the offset protocol, not just `SimpleException`.

### `@raise_location_offset` (Decorator)

For utility and validation functions, use this decorator to automatically shift exception origins to the caller.

```python
from simplibs.exception import raise_location_offset

@raise_location_offset(offset=1)
def validate_age(age):
    if age < 0:
        raise SimpleException(
            value=age,
            problem="age cannot be negative"
        )

# Error now points HERE, not inside validate_age()
validate_age(-5)
```

When the decorated function raises an exception with `with_location_offset` support, the decorator intercepts it, applies the offset, and re-raises it with `from None`. This suppresses the "During handling..." message and keeps your traceback clean and focused on what actually matters — where the caller invoked your function.

Like `raise_with_location_offset()`, the decorator uses duck typing, so it works with any exception class that implements the offset protocol.

---

## Serialization

Need to send errors over the wire or log them structurally?

```python
e = SimpleException(
    label="user_id",
    value=None,
    problem="user not found"
)

# Get a clean dictionary (UNSET values omitted)
e.to_dict()
# {'error_name': 'ERROR', 'label': 'user_id', ...}

# Get JSON for APIs
e.to_json()
# '{"error_name": "ERROR", ...}'

# Get everything (internal state included)
e.to_debug_dict()
```

---

## Global Settings

Configuration in `simplibs-exception` works at multiple levels. Understand the hierarchy, and you'll have complete control over how your exceptions behave.

### Understanding the Configuration Hierarchy

Settings can be controlled at three levels, each with increasing precedence:

**Level 1: Global defaults** (`SimpleExceptionSettings`)
The foundation — applies to all exceptions in your application.

```python
from simplibs.exception import SimpleExceptionSettings

SimpleExceptionSettings.DEFAULT_GET_LOCATION = False  # Disable location tracking globally
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = SIMPLE  # Use plain text everywhere
```

**Level 2: Class-level defaults** (custom exception subclass)
Overrides global defaults for a specific exception type.

```python
class MyValidationError(SimpleException):
    error_name = "VALIDATION ERROR"
    skip_locations = ("mylib/",)  # This class always skips mylib/ paths
    how_to_fix = ("Check the input format.",)
```

**Level 3: Instance-level overrides** (parameters at raise time)
Takes precedence over everything — the most specific, for a single exception.

```python
raise MyValidationError(
    value=age,
    get_location=2,  # Override global setting just for this exception
    skip_locations=("mylib/", "vendor/")  # Add to or override class default
)
```

**Priority order** (highest to lowest):
```
Instance parameter > Class default > Global setting > Built-in default
```

### Configurable Parameters

Here's what can be configured at each level:

| Parameter | Global | Class | Instance | Type | Description |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `DEFAULT_GET_LOCATION` | ✅ | ✅ | ✅ | `bool` or `int` | Enable/disable file location tracking or set stack depth |
| `DEFAULT_LOCATION_BLACKLIST` | ✅ | ✅ | ✅ | `tuple[str,...]` | Path patterns to skip during stack walk — patterns merge together |
| `DEFAULT_MESSAGE_MODE` | ✅ | ❌ | ⚠️ | `ModeBase` instance | Output format (PRETTY, SIMPLE, ONELINE, LOG, or custom) |
| `DEFAULT_VALUE_TRUNCATION_LENGTH` | ✅ | ❌ | ❌ | `int` | Character limit for value display before truncation |

**Legend:**
- ✅ Can be set at this level
- ❌ Cannot be set at this level
- ⚠️ Use `oneline=True` parameter instead of changing the mode

### Getting Location Information

`DEFAULT_GET_LOCATION` controls whether and how the exception reports its origin.

| Value | Behavior | Example |
| :--- | :--- | :--- |
| `False` | Location not reported | No "File info" line in output |
| `True` (default) | First non-excluded frame | Points to user code, skips library internals |
| `1` | Same as `True` | Explicit stack depth 1 |
| `2`, `3`, ... | Second, third non-excluded frame | Advanced: skip additional layers |

**Global configuration:**

```python
from simplibs.exception import SimpleExceptionSettings

# Disable location tracking entirely
SimpleExceptionSettings.DEFAULT_GET_LOCATION = False

# Or set to a specific depth
SimpleExceptionSettings.DEFAULT_GET_LOCATION = 2
```

**Per-exception override:**

```python
raise SimpleException(
    problem="Something went wrong",
    get_location=False  # Just this exception won't show location
)
```

**In a custom exception class:**

```python
class MyError(SimpleException):
    _get_location = False  # All instances of MyError hide their location
```

### Filtering Library Code from Stack Traces

`DEFAULT_LOCATION_BLACKLIST` tells the exception to skip over your library's internal frames and point to the user's code instead. For detailed information on how this works, see [Advanced: Stack Filtering for Library Development](#advanced-stack-filtering-for-library-development).

**Global configuration:**

```python
SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST = (
    "mylib/",
    "mylib_helpers/",
    "vendor/internal/"
)
```

**Per-exception override:**

```python
raise SimpleException(
    problem="Something went wrong",
    skip_locations=("mylib/validators/",)  # Skip only this for this exception
)
```

**In a custom exception class:**

```python
class ValidationError(SimpleException):
    skip_locations = ("mylib/",)  # All instances skip mylib/
```

**How patterns work:**
- Patterns are matched as substrings against the full file path
- All patterns from global + class + instance are merged together
- If a frame's path contains *any* pattern, it's skipped
- The function returns the **last frame it saw** as a fallback — even if all frames match the blacklist

Example:
```python
# Global
SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST = ("mylib/",)

# Class
class MyError(SimpleException):
    skip_locations = ("helpers/",)

# Instance
raise MyError(skip_locations=("vendor/",))

# Result: all three patterns apply
# Frames are skipped if they contain: "mylib/" OR "helpers/" OR "vendor/"
```

### Output Modes

`DEFAULT_MESSAGE_MODE` determines the default format for all exceptions.

**Available built-in modes:**

```python
from simplibs.exception import SimpleExceptionSettings, PRETTY, SIMPLE, ONELINE, LOG

SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = PRETTY    # Framed output (default)
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = SIMPLE    # Plain text, no decorations
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = ONELINE   # Compact single-line format
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = LOG       # key=value for log parsers
```

**Using a custom mode:**

```python
from simplibs.exception import SimpleExceptionSettings, ModeBase

class SlackMode(ModeBase):
    def _full_outcome(self, data):
        return f":warning: *{data.error_name}*\nProblem: {data.problem}"

SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = SlackMode()
```

**Per-exception override:**

You can't change the mode for a single exception globally, but you can use `oneline=True` to force compact output:

```python
raise SimpleException(
    problem="Something went wrong",
    oneline=True  # Forces ONELINE mode just for this exception
)
```

### Value Truncation

`DEFAULT_VALUE_TRUNCATION_LENGTH` sets the maximum length of a value's string representation before it gets cut off.

**Global configuration:**

```python
SimpleExceptionSettings.DEFAULT_VALUE_TRUNCATION_LENGTH = 100  # Show up to 100 chars

raise SimpleException(
    value=very_long_data_structure,
    problem="Data is invalid"
)
# Output: Got: "{'key': 'value', 'nested': {...}}... [truncated, 450 chars]" (dict)
```

If a value is longer than the limit, it displays the first N characters and shows how many were omitted:

```
Got: "[1, 2, 3, 4, 5, ... lots more items ... ]... [truncated, 892 chars]" (list)
```

**Why?** Large data structures (deep nested objects, huge lists, long strings) can overwhelm terminal output. Truncation keeps the display readable.

**Recommended values:** 50–200 depending on your terminal width and preference.

### Resetting to Factory Defaults

If you've changed global settings and want to restore them:

```python
from simplibs.exception import SimpleExceptionSettings

SimpleExceptionSettings.reset()

# Now all settings are back to:
# DEFAULT_GET_LOCATION = 1
# DEFAULT_LOCATION_BLACKLIST = ("simplibs/exception",)
# DEFAULT_MESSAGE_MODE = PRETTY
# DEFAULT_VALUE_TRUNCATION_LENGTH = 70
```

### Validation & Safety

`SimpleExceptionSettings` uses a **metaclass** (`SimpleExceptionSettingsMeta`) that validates every attribute assignment. This means:

✅ **Type safety** — You can't accidentally assign a wrong type:
```python
# This raises SimpleExceptionSettingsError
SimpleExceptionSettings.DEFAULT_GET_LOCATION = "true"  # ❌ string, not bool/int
```

✅ **Typo protection** — You can't create new attributes by mistake:
```python
# This raises SimpleExceptionSettingsError
SimpleExceptionSettings.DEFUALT_GET_LOCATION = True  # ❌ typo in attribute name
```

✅ **Range validation** — Integer values must be sensible:
```python
# This raises SimpleExceptionSettingsError
SimpleExceptionSettings.DEFAULT_VALUE_TRUNCATION_LENGTH = -10  # ❌ must be positive
```

✅ **Structure validation** — Complex types are checked:
```python
# This raises SimpleExceptionSettingsError
SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST = "mylib/"  # ❌ must be tuple, not string
```

If any assignment is invalid, you get a clear `SimpleExceptionSettingsError` explaining what went wrong and how to fix it.

### Complete Example: Multi-Level Configuration

Here's a realistic setup showing all three levels working together:

```python
from simplibs.exception import SimpleException, SimpleExceptionSettings, SIMPLE

# ============================================================================
# Level 1: Global defaults (for the entire application)
# ============================================================================
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = SIMPLE
SimpleExceptionSettings.DEFAULT_VALUE_TRUNCATION_LENGTH = 150
SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST = ("myapp/", "myapp_internals/")

# ============================================================================
# Level 2: Custom exception class (for a family of related errors)
# ============================================================================
class ValidationError(SimpleException):
    error_name = "VALIDATION ERROR"
    skip_locations = ("validators/", "schema/")  # Additional patterns for this class
    expected = "valid input"
    how_to_fix = (
        "Check the input format against the documentation.",
        "Run the validation debug tool: python -m myapp.tools validate",
    )

# ============================================================================
# Level 3: Instance-level (for a specific exception)
# ============================================================================
def process_user_data(data):
    try:
        validate_email(data['email'])
    except ValidationError:
        # Re-raise with custom configuration just for this case
        raise ValidationError(
            value=data['email'],
            label="user email",
            get_location=False,  # Hide location for this one
            skip_locations=("email_validators/",)  # Add more patterns
        )

# Result:
# - Uses SIMPLE mode (global)
# - Values truncated to 150 chars (global)
# - Skips myapp/, myapp_internals/, validators/, schema/, email_validators/
#   (merge of global + class + instance)
# - No location shown (instance override of global True)
```

### Common Mistakes & How to Avoid Them

❌ **Mistake: Assigning a string instead of a tuple**
```python
SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST = "mylib/"  # Wrong!
```

✅ **Fix:**
```python
SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST = ("mylib/",)  # Tuple with one item
```

---

❌ **Mistake: Trying to set a mode on a single exception**
```python
raise SimpleException(message="Oops", DEFAULT_MESSAGE_MODE=ONELINE)  # No such parameter!
```

✅ **Fix:**
```python
raise SimpleException(message="Oops", oneline=True)  # Use oneline instead
```

---

❌ **Mistake: Forgetting to instantiate a custom mode**
```python
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = SlackMode  # Wrong! (class, not instance)
```

✅ **Fix:**
```python
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = SlackMode()  # Correct (instance)
```

---

## Advanced: Stack Filtering for Library Development

When you're building a library, your own internal code sits between the user's code and the exception. By default, `get_location=True` will point to your library's internals — not helpful for the user. This section shows how to fix that.

### How Stack Filtering Works

When `get_location=True` (or an integer), the exception walks the call stack and looks for the first frame that **isn't** in `skip_locations`. Here's the flow:

1. Extract the full call stack
2. Iterate through each frame, starting from the innermost (closest to the error)
3. Normalize all paths to POSIX format for cross-platform matching
4. For each frame, check if its path contains any string in `skip_locations`
5. If the frame is **not excluded**, increment the "valid frame" counter
6. When the counter reaches the value of `get_location` (default: 1), return that frame's info

The key insight: `get_location=1` means "first non-excluded frame", `get_location=2` means "second non-excluded frame", and so on.

### The Fallback: Safety Net for Libraries

If you've excluded so much code that no valid frames remain, the exception doesn't give up. Instead:

- It keeps track of the **last frame it saw** while walking the stack
- If the counter never reaches the requested level, it returns that final frame
- Result: You always get *some* useful context, even in deeply nested calls

This is intentional. For library developers, it means:

**Even if all frames in the stack are from your library, the exception will show the innermost one** — which is often the most relevant for debugging.

### Example: Building a Validation Library

Imagine you're writing a validation library with this structure:

```
myvalidation/
  __init__.py
  validators.py      ← internal validation logic
  exceptions.py      ← exception definitions
```

When a user calls your validator and it fails, the stack might look like:

```
user_code.py (line 42)           ← User's code (target!)
  └─ myvalidation/__init__.py    ← Entry point
      └─ myvalidation/validators.py
          └─ raise ValidationError
```

Without filtering, the error points to `myvalidation/validators.py` — not useful.

**Solution:** Define your exception class with `skip_locations`:

```python
from simplibs.exception import SimpleException

class ValidationError(SimpleException):
    error_name = "VALIDATION ERROR"
    skip_locations = ("myvalidation/",)  # Skip all internal paths
    how_to_fix = "Review the validation rules for this field."

# Usage in your validator
def validate_email(email):
    if "@" not in email:
        raise ValidationError(
            value=email,
            label="email",
            expected="a valid email address",
            problem="missing @ symbol"
        )
```

Now when a user calls it:

```python
from myvalidation import validate_email

validate_email("invalid")  # Error points HERE (user_code.py), not inside your library
```

### Global vs. Instance-Level Filtering

You can set `skip_locations` at different levels:

**Class-level** (affects all instances):

```python
class MyError(SimpleException):
    skip_locations = ("mylib/",)
```

**Instance-level** (affects only this exception):

```python
raise SimpleException(
    skip_locations=("mylib/", "helpers/"),
    problem="Something went wrong"
)
```

**Global** (affects all exceptions everywhere):

```python
from simplibs.exception import SimpleExceptionSettings

SimpleExceptionSettings.DEFAULT_LOCATION_BLACKLIST = ("mylib/", "vendor/")
```

Patterns are merged: instance + class + global all apply together. This gives you fine control at every level.

### Controlling Location Display

If you want to disable file location tracking entirely:

```python
# Global — no location info for any exception
SimpleExceptionSettings.DEFAULT_GET_LOCATION = False

# Per-exception — just this one
raise SimpleException(
    get_location=False,
    problem="Something went wrong"
)
```

With `get_location=False`, the "File info" and "File path" lines are omitted from the output.

### Why This Matters

For library users, seeing `File: myvalidation/validators.py | Line: 87` is noise. They want to know:

- What they passed in (the `value`)
- What went wrong (the `problem`)  
- How to fix it (the `how_to_fix`)
- Where *in their code* to look

By filtering out your library's internals with `skip_locations`, you give users exactly that — a clear, actionable error report that points to *their* code, not yours.

---

## Custom Output Modes

Instead of being locked into predefined formats, you can build your own exception output mode tailored to your needs — Slack notifications, JSON APIs, custom terminals, or anything else.

### Understanding the Data Structure

Every mode receives a `SimpleExceptionData` object containing all information about the exception. Here's what you have access to:

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `error_name` | `str` | The error label (e.g., `"VALIDATION ERROR"`) |
| `exception` | `type[Exception]` or `UNSET` | The exception class for catching |
| `value` | `object` | The actual value that caused the problem |
| `label` | `str` or `UNSET` | Human label for that value (e.g., `"parameter age"`) |
| `expected` | `str` or `UNSET` | What you wanted to see |
| `problem` | `str` or `UNSET` | What went wrong |
| `context` | `str` or `UNSET` | Extra situational info |
| `message` | `str` or `UNSET` | Free-form message (alternative to structured fields) |
| `how_to_fix` | `tuple[str, ...]` or `UNSET` | Remediation tips |
| `caller_info` | `dict` or `None` | Location info: `file`, `line`, `full_path`, `function` |
| `_get_location` | `bool` or `int` | Whether location tracking is enabled |
| `_intercepted_exception` | `str` or `UNSET` | Message from a caught exception (if wrapped) |

Check any attribute with the sentinel `UNSET` before using it — if it's `UNSET`, the user didn't provide that field.

### The Three Outcome Methods

Your mode must implement one method, but can optionally implement two others for richer control:

#### `_full_outcome(data: SimpleExceptionData) -> str` — **Required**

Called when the exception has structural content (value, expected, problem, how_to_fix, etc.). This is where you build the main detailed output.

```python
def _full_outcome(self, data: SimpleExceptionData) -> str:
    """Full diagnostic output with all available fields."""
    parts = [
        f"Error: {data.error_name}",
        f"Value: {data.value}",
        f"Expected: {data.expected}",
        f"Problem: {data.problem}",
    ]
    return "\n".join(p for p in parts if p)
```

#### `_message_outcome(data: SimpleExceptionData) -> str` — *Optional*

Called when only a `message` is provided, with no structured fields. If you don't define it, `ModeBase` provides a default:

```python
def _message_outcome(self, data: SimpleExceptionData) -> str:
    """Simple message-only output."""
    return f"⚠️ {data.error_name}: {data.message}"
```

#### `_empty_outcome(data: SimpleExceptionData) -> str` — *Optional*

Called when the exception has no data at all — just marking a location. If you don't define it, `ModeBase` provides a default:

```python
def _empty_outcome(self, data: SimpleExceptionData) -> str:
    """Minimal output — only the error name and location."""
    return f"⚠️ {data.error_name}"
```

**Only `_full_outcome()` is abstract — you must implement it.** For `_empty_outcome()` and `_message_outcome()`, the base class provides sensible defaults. Override them only if you want custom behavior.

### Helper Methods (Mixins)

`ModeBase` provides three helper methods via mixins. Use them to format data consistently:

#### `_print_intro_line(data: SimpleExceptionData) -> str`

Builds the opening line with error name and optional value label:

```python
self._print_intro_line(data)
# Returns: "⚠️ VALIDATION ERROR: parameter age"
# Or:      "⚠️ VALIDATION ERROR" (if no label)
```

#### `_print_caller_info(data: SimpleExceptionData, *, as_dict: bool = False) -> str | dict`

Formats file location information. Set `as_dict=True` for structured output (useful for LOG mode):

```python
# Human-readable string
self._print_caller_info(data)
# Returns: "File: main.py | Line: 42 | Path: /path/to/main.py | Function: validate"

# Machine-readable dictionary
self._print_caller_info(data, as_dict=True)
# Returns: {'file': 'main.py', 'line': 42, 'path': '/path/to/main.py', 'func': 'validate'}
```

Returns `"Location: Unknown"` if location tracking is disabled or fails.

#### `_print_value_with_type(data: SimpleExceptionData, *, intro: str = "", max_length: int | None = None) -> str | None`

Formats the inspected value with its type. Returns `None` if no value was provided.

```python
# Full representation with intro prefix
self._print_value_with_type(data, intro="Got: ")
# Returns: 'Got: -5 (int)'

# With custom truncation limit
self._print_value_with_type(data, intro="Value: ", max_length=50)
# Returns: 'Value: "this is a very long string that gets cut off... [truncated, 120 chars]" (str)'
```

If `max_length` is not provided, uses the global `SimpleExceptionSettings.DEFAULT_VALUE_TRUNCATION_LENGTH` (default: 70 chars).

### Example: Building a Custom Mode

Here's a practical example — a Slack-friendly mode that formats exceptions as structured blocks:

```python
from simplibs.exception import ModeBase, SimpleExceptionData
from simplibs.sentinels import UNSET

class SlackMode(ModeBase):
    """Exception output formatted for Slack messages."""

    def _full_outcome(self, data: SimpleExceptionData) -> str:
        """Build a Slack-friendly message with sections."""
        blocks = [
            f":warning: *{data.error_name}*"
        ]

        # Add structured fields if present
        if data.label:
            blocks.append(f"*Value:* `{data.label}`")

        if data.value is not UNSET:
            blocks.append(f"*Got:* {self._print_value_with_type(data)}")

        if data.expected:
            blocks.append(f"*Expected:* {data.expected}")

        if data.problem:
            blocks.append(f"*Problem:* {data.problem}")

        # Add remediation
        if data.how_to_fix:
            fixes = "\n".join(f"• {tip}" for tip in data.how_to_fix)
            blocks.append(f"*Fix:*\n{fixes}")

        # Add location if available
        loc = self._print_caller_info(data, as_dict=True)
        if loc and loc['file'] != "unknown":
            blocks.append(f"*File:* `{loc['file']}:{loc['line']}`")

        return "\n".join(blocks)

    def _message_outcome(self, data: SimpleExceptionData) -> str:
        """Simplified output for message-only exceptions."""
        return f":warning: *{data.error_name}*\n{data.message}"

    def _empty_outcome(self, data: SimpleExceptionData) -> str:
        """Minimal output."""
        return f":warning: {data.error_name}"
```

**Key patterns:**
- Check fields against `UNSET` before using them
- Use helper methods (`_print_intro_line()`, `_print_caller_info()`, `_print_value_with_type()`)
- Return a string in your chosen format
- Handle all three outcomes gracefully

### Registering Your Mode

Once you've built your mode, register it globally so all exceptions use it:

```python
from simplibs.exception import SimpleExceptionSettings

# Create an instance of your mode
slack_mode = SlackMode()

# Set it as the default
SimpleExceptionSettings.DEFAULT_MESSAGE_MODE = slack_mode

# Now every exception uses your mode
raise SimpleException(
    value=age,
    problem="age cannot be negative"
)
# Output will be formatted by SlackMode._full_outcome()
```

Or use it just for one exception:

```python
from simplibs.exception import SimpleException

raise SimpleException(
    value=age,
    problem="age cannot be negative",
    # Force ONELINE mode just for this exception
    oneline=True
)
```

### Important: Modes Must Not Reference Settings

When building a custom mode, **do not import or reference `SimpleExceptionSettings`** directly (except for accessing global values like `DEFAULT_VALUE_TRUNCATION_LENGTH` through the helper methods).

The design is intentional: settings consume modes, never the other way around. This prevents circular dependencies and keeps modes reusable and independent.

✅ **Good:**
```python
# Use helper methods that internally access settings
max_len = S.DEFAULT_VALUE_TRUNCATION_LENGTH  # Inside a helper, not your mode
```

❌ **Bad:**
```python
# Don't reference settings in your mode directly
from simplibs.exception import SimpleExceptionSettings
class MyMode(ModeBase):
    def _full_outcome(self, data):
        # This creates a circular dependency
        if SimpleExceptionSettings.DEFAULT_GET_LOCATION:
            ...
```

---

## About simplibs

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

`simplibs-exception` is the foundation of the **simplibs** ecosystem — it gives
the ecosystem a voice, helping it communicate with the user in a clear and
human way: not just reporting what went wrong, but pointing towards a fix.
The name *simplibs* is short for *simple libraries*.

*The library is covered by tests across all modules — unit tests and
integration tests alike. Tests are part of the repository and serve
as living documentation of the expected behaviour.*

---

## Reference

### Full Parameter Table

```python
SimpleException(
    # Core diagnostic fields (all optional)
    message="...",                      # Alternative to structured fields
    label="...",                  # What thing broke?
    value=any_object,                   # The actual value
    expected="...",                     # What you wanted
    problem="...",                      # What went wrong
    context="...",                      # Extra info
    how_to_fix="..." or ("tip1", "tip2"),  # How to fix

    # Control & customization
    error_name="ERROR",                 # Custom error label
    exception=ValueError,               # Catchable as this type
    get_location=True,                  # Track file/line? (True/False/int)
    skip_locations=("file.py",),        # Ignore these files
    oneline=False,                      # Single-line output?
)
```

---

## License

MIT. Build great things.