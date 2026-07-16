# 🎯`simplibs-exception`

[![PyPI](https://img.shields.io/pypi/v/simplibs-exception)](https://pypi.org/project/simplibs-exception/) 
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/) 
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-exception/blob/main/LICENSE)

**An exception that tries to be a friend.**

A structured Python exception framework that doesn't just crash—it explains what went wrong, 
why it happened, and how to fix it. Beautiful terminal layouts, programmatic analytics exporters, zero filler.

```text
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

## 🧭 The Core Philosophy

Standard Python exceptions tell you *where* code broke, but they leave you guessing 
about *what* was inside your variables or *how* to recover. You end up stuffing 
complex debugging telemetry into ad-hoc f-strings.

`simplibs-exception` changes the paradigm. Instead of chaotic crashes, 
you get **diagnostic reports**: highly structured, easily readable context 
containing your expected vs. obtained values, specific problem statements, 
and actionable remediation steps.

---

## 📦 Installation

```bash
pip install simplibs-exception
```
> ⚠️ **Migration Note (v0.2.x → v1.0.0+):**  
> Please note that version `1.0.0` and above introduces a breaking change and is not backward compatible with previous releases. The parameter `value_label` in `SimpleExceptionData` (and `SimpleException`) has been renamed to `label` for greater semantic precision and broader context applicability. If you are upgrading from an older version, please update your codebase accordingly.


---

## 🚀 Quick Start in 60 Seconds

You can initialize `SimpleException` as an empty marker and enrich it incrementally. 
**All parameters are optional.**

### Level 1: The Marker

Just mark a failure point—the framework automatically captures file, line, and function context.

```python
from simplibs.exception import SimpleException

raise SimpleException()
# ⚠️ ERROR: File: main.py | Line: 12 | Function: process
```

### Level 2: Custom Text Message

Use it like a traditional exception but wrapped in cleaner console formatting.

```python
raise SimpleException("Database connection timed out after 30s")
```

### Level 3: The Full Diagnostic

Provide full structured data to turn a simple crash into an elite debugging card.

```python
raise SimpleException(
    label      = "parameter age",
    expected   = "a positive integer",
    value      = age,
    problem    = "value is negative",
    how_to_fix = "Provide a value greater than 0."
)
```

---

## 🛠️ The Architecture: 3 Pillars

To keep the library clean and highly optimized, the logic is separated into three decoupled components:

```
┌────────────────────────────────┐
│   SimpleExceptionSettings      │ ◄── Global configuration, overrides, and safety locks
└──────────────┬─────────────────┘
               │
               ▼
┌────────────────────────────────┐
│      SimpleExceptionData       │ ◄── Immutable data storage, serializers (.to_dict())
└──────────────┬─────────────────┘
               │
               ▼
┌────────────────────────────────┐
│        SimpleException         │ ◄── Active runtime manager, dynamic MRO, and execution
└────────────────────────────────┘
```

### 1. `SimpleExceptionData` (The Model)

Acts as the passive data schema. It owns the raw parameters, lazy caching properties, 
and public analytics state exporters (`to_dict()`, `to_json()`).

➡️ [README_DATA.md](https://github.com/simplibs/simplibs-exception/blob/main/docs/README_DATA.md)

### 2. `SimpleException` (The Runtime Engine)

The active execution manager. It overrides dataclass-level `__init__` routines, 
manages dynamic Method Resolution Order (MRO) injection, triggers subclass compile-time audits, 
and orchestrates terminal rendering.

➡️ [README_EXCEPTION.md](https://github.com/simplibs/simplibs-exception/blob/main/docs/README_EXCEPTION.md)

### 3. `SimpleExceptionSettings` (The Control Center)

A validated global configuration interface governed by a strict metaclass. 
It lets you customize default behaviors, set value truncation boundaries, 
and control stack trace filtering securely.

➡️ [README_SETTINGS.md](https://github.com/simplibs/simplibs-exception/blob/main/docs/README_SETTINGS.md)

---

## 🎨 Output Modes

Your exception can speak different visual formats depending on your deployment environment:

* **`PRETTY` (Default):** 
Beautifully framed visual card layout optimized for console output during development.
* **`SIMPLE`:** 
Plain-text structured layout without Unicode borders. Perfect for standard files and log processors.
* **`ONELINE`:** 
Everything compressed into a single line. Perfect for standard application log streaming.
* **`LOG`:** 
Highly optimized, machine-readable `key=value` format designed for log forwarders (Datadog, Splunk, ELK).

➡️ [README_MODES.md](https://github.com/simplibs/simplibs-exception/blob/main/docs/modes/README_MODES.md)

You can easily build your own layout formats (e.g., HTML, Slack message blocks) by subclassing the base template manager `ModeBase`.

➡️ [README_CUSTOM_MODES.md](https://github.com/simplibs/simplibs-exception/blob/main/docs/modes/README_CUSTOM_MODES.md)

---

## 🧰 Built-in Developer Tools

The framework provides helper functions to minimize repetitive error-handling boilerplate:

### `bool_or_exception`

A bi-modal validation shortcut. It either gracefully returns `False` 
or raises a fully-structured exception based on a flag, eliminating verbose conditional block code.

```python
from simplibs.exception.tools import bool_or_exception

def validate_age(age: int, return_bool: bool = False) -> bool:
    if age < 0:
        return bool_or_exception(return_bool, value=age, label="age", expected="positive integer")
    return True
```

➡️ [README_BOOL_OR_EXCEPTION.md](https://github.com/simplibs/simplibs-exception/blob/main/docs/tools/README_BOOL_OR_EXCEPTION.md)

### `raise_with_location_offset`

A single-line utility that takes any exception, dynamically shifts its stack trace 
tracking depth backwards, and raises it.

```python
raise_with_location_offset(SimpleException("Failed"), offset=1)
```

➡️ [README_RAISE_WITN_LOCATION_OFFSET.md](https://github.com/simplibs/simplibs-exception/blob/main/docs/tools/README_RAISE_WITN_LOCATION_OFFSET.md)

### `@raise_location_offset` (Decorator)

An Aspect-Oriented decorator that intercepts bubbling exceptions and re-targets 
their trace location to the caller's call-site. Excellent for writing transparent 
gatekeeper and validator helpers.

```python
@raise_location_offset(offset=1)
def assert_positive(n: int):
    if n <= 0:
        raise SimpleException(value=n, expected="strictly positive")
```

➡️ [README_RAISE_LOCATION_OFFSET.md](https://github.com/simplibs/simplibs-exception/blob/main/docs/tools/README_RAISE_LOCATION_OFFSET.md)

---

## 🧪 Advanced Testing Ecosystem

Writing unit tests for custom exceptions, validation functions, and error parameters 
often leads to repetitive boilerplate. To solve this, `simplibs-exception` includes 
a **complete, self-contained testing framework** under its `testing` namespace.

With our testing tools, you can run bulk matrix-driven evaluations, validate class MRO integrity, 
and audit error payloads with minimal code:

```python
from simplibs.exception.testing import assert_exception_class

# Automatically audits inheritance, defaults, constructors, and serialization protocols
assert_exception_class(MyCustomError)
```

➡️ [README_TESTING.md](https://github.com/simplibs/simplibs-exception/blob/main/docs/testing/README_TESTING.md)

---

## ☯️ About simplibs

All libraries in the **simplibs** (Simple Libraries) ecosystem share a common engineering philosophy:

* **Dyslexia-friendly:** 
We actively minimize cognitive load. Code is atomized into small, self-contained units, 
files are named directly after the logical task they perform, 
and explanations describe *why* something is designed, not just *what* it is.
* **Programmer's Zen:** 
Nothing should be missing, and nothing should be superfluous. 
We value clean execution paths and robust, understandable code architectures over rushed, messy feature sets.
* **Defensive Style:** 
We actively anticipate edge cases and failure modes so that only safe operational paths remain. 
Our code is built to degrade gracefully rather than crash unexpectedly.
* **Minimalism:** 
Find the most direct path to the goal in as few operational steps as possible 
without taking shortcuts on safety, readability, or completeness.
* **Code as Craft:** 
Code should be pleasant to look at, readable at a glance, and evoke structural harmony. 
We treat software engineering as a precision trade.

---

### 🤝 Contributing & Community

This is an **open-source project** built with love and care. 
We strongly believe in community collaboration and welcome any feedback, bug reports, or feature ideas!

* **Want to contribute?** Feel free to open an Issue or submit a Pull Request.
* **Want to get in touch?** If you'd like to discuss the project further, collaborate,
or just say hello, feel free to open a GitHub Issue or start a Discussion.

---

### 📝 License

This library is released under the **MIT License**. Build great things!

---

[▲ Back to Top](#simplibs-exception)