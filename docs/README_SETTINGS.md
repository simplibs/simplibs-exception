# ✨ `SimpleExceptionSettings`

**The Central Configuration Registry and Single Source of Truth for Exception Behavior**

The `SimpleExceptionSettings` class serves as a global, runtime configuration registry 
that governs the behavior, traceback resolution, and layout formatting of all exceptions 
within your project ecosystem. 
All settings are stateful and can be dynamically modified at runtime or restored to factory defaults 
with a single method call.

The class functions strictly as a static namespace and is **intentionally protected against instantiation**.

> 💡 **Table of Contents:**
> * [⚙️ Architectural Concept and Role](#-architectural-concept-and-role)
> * [🛠️ Configuration and Attributes](#-configuration-and-attributes)
> * [🧪 Robust Validation and SettingsMeta](#-robust-validation-and-settingsmeta)
> * [📖 Real-World Cookbooks](#-real-world-cookbooks)


---

## ⚙️ Architectural Concept and Role

* **Monolithic Static Namespace:** 
The configuration registry cannot be instantiated. 
Any attempt to invoke `SimpleExceptionSettings()` raises a specific `SimpleExceptionSettingsError` 
equipped with clear, actionable guidelines on how to interact with settings correctly.
* **Type and Value Safety:** 
Every attempt to write a configuration attribute is intercepted at the metaclass layer 
and subjected to strict validation. Typos in attribute names or invalid data types 
are eliminated immediately before they can impact downstream runtime flows.
* **One-Way Dependency (Circular Guardrail):** 
The settings registry consumes layout presentation modes (e.g., `PRETTY`), 
but presentation modes themselves must remain completely agnostic of the settings registry. 
This strict architectural design pattern prevents circular package initialization loops.

---

## 🛠️ Configuration and Attributes

Below is the configuration registry class interface, followed by a detailed description of each property.

```python
class SimpleExceptionSettings:
    # --- System Blacklist (Read-Only) ---
    _SYSTEM_BLACKLIST: tuple[str, ...] = ("<", "simplibs/exception")

    # --- Live Configuration Attributes ---
    GET_LOCATION: int | bool = 1
    LOCATION_BLACKLIST: tuple[str, ...] = _SYSTEM_BLACKLIST
    MESSAGE_MODE: ModeBaseProtocol = PRETTY
    VALUE_TRUNCATION_LENGTH: int = 70

    # --- Internal Cache (Read-Only Reset) ---
    _dynamic_cls_cache: dict = {}
```

### 📋 Settings Attribute Matrix

| Attribute                 | Data Type         | Default Value       | Description                                                                                  |
| :------------------------ | :---------------- | :------------------ | :------------------------------------------------------------------------------------------- |
| `GET_LOCATION`            | `int` / `bool`    | `1`                 | Controls the activation state and stack traversal depth scanner for the error line.          |
| `LOCATION_BLACKLIST`      | `tuple[str, ...]` | `_SYSTEM_BLACKLIST` | User-defined list of directories, packages, or file patterns skipped during stack analysis.  |
| `MESSAGE_MODE`            | `ModeBase`        | `PRETTY`            | The default presentation mode used to format the final exception text output.                |
| `VALUE_TRUNCATION_LENGTH` | `int`             | `70`                | The maximum allowed character length of an inspected runtime value (`value`) representation. |

> **`_SYSTEM_BLACKLIST`** == ("<", "simplibs/exception")  
> These patterns exclude Python internal frames and the `simplibs.exception`
> implementation itself from automatic caller location detection.

---

### 🔍 Detailed Attribute Descriptions

#### `_SYSTEM_BLACKLIST` (System-Protected Blacklist – Read-Only)

A system-protected tuple containing file patterns that are unconditionally skipped during traceback frame analysis.

* Contains `"<"` to ignore Python's dynamic virtual stack frames 
(e.g., `<string>`, `<lambda>`, `<frozen importlib>`).
* Contains `"simplibs/exception"` to automatically filter out internal framework execution paths, 
ensuring error outputs remain clean.
* *Note: This attribute is strictly read-only and is heavily protected against manual modification 
or runtime overrides at the metaclass layer.*

#### `GET_LOCATION`

Specifies how deeply the traceback engine should traverse the call stack to find 
the original source of the exception.

* `False` ➔ Completely disables location reporting (the `caller_info` property resolves to `None`).
* `True` ➔ Captures the immediate external user code frame that initialized the error (Depth: `1`).
* `int` (e.g., `2`, `3`) ➔ Configures a fixed vertical depth offset. Value must be `>= 0`.

#### `LOCATION_BLACKLIST`

A tuple of strings representing directory paths, package namespaces, or file names you want to skip 
during call-stack traversal (e.g., auxiliary wrappers, route controllers, or third-party decorators). 
The scanning engine automatically merges these patterns with `_SYSTEM_BLACKLIST` during traceback processing.

#### `MESSAGE_MODE`

An instance of a class inheriting from `ModeBase`. It controls the default layout configuration. 
You can assign any of the four built-in singletons (`PRETTY`, `SIMPLE`, `ONELINE`, `LOG`) 
or hook up your own custom-engineered presentation style.

#### `VALUE_TRUNCATION_LENGTH`

An integer (must be strictly `> 0`) specifying the text limit for the inspected target 
value representation (`data.value`). If the string representation length exceeds this threshold, 
the value is truncated and appended with a safe token counter (e.g., `[truncated, 150 chars]`). 
This prevents logs and terminals from being flooded by massive dictionary payloads or database dumps.

[🔼 Back to Top](#-simpleexceptionsettings)

---

## 🧪 Robust Validation and `SettingsMeta`

The integrity of the settings registry is maintained by the `SettingsMeta` metaclass. 
Every state modification (the `__setattr__` operation) is routed through a validation firewall. 
If any rule is violated, it immediately raises a descriptive `SimpleExceptionSettingsError` 
providing explicit instructions for correction:

### 🛡️ Core Metaclass Validation Rules

1. **System Blacklist Lock:**  
Any attempt to mutate `_SYSTEM_BLACKLIST` fails instantly.   
Developers are directed to append custom files or repository paths to `LOCATION_BLACKLIST` instead.
2. **Typo Prevention (Strict Whitelisting):** 
If you attempt to write to an unmapped attribute (e.g., `SimpleExceptionSettings.GET_LOCATON = True`), 
the metaclass blocks the operation, identifies the typo, and lists all permissible operational settings.
3. **`GET_LOCATION` Type Guard:** 
Restricts values strictly to `bool` or non-negative integers (`int`).  
Negative offsets are rejected because they are unsupported by Python's stack frame inspection utilities.
4. **`LOCATION_BLACKLIST` Integrity:** 
Enforces a strict `tuple` type containing exclusively string (`str`) elements.  
If a list, raw string, or a tuple containing invalid types (like `None` or `int`) is supplied, 
validation fails and reports the exact count of invalid elements detected.
5. **`MESSAGE_MODE` Inheritance Verification:** 
Requires that assigned objects derive strictly from `ModeBase`.  
Any other formatting objects or structures are rejected.
6. **`VALUE_TRUNCATION_LENGTH` Boundary Check:** 
Requires a positive integer (`int`) strictly greater than `0`.  
Boolean values (`True`/`False`), although technically treated as integer subclasses in Python, 
are explicitly blocked.
7. **Cache Modification Protection (`_dynamic_cls_cache`):** 
Restricts writes to an empty dictionary `{}` only—permitting cache clears during hot-reloads 
or unit tests while preventing manual injection of unvalidated class mappings.

[🔼 Back to Top](#-simpleexceptionsettings)

---

## 📖 Real-World Cookbooks

The following recipes demonstrate how to interact with the configuration registry 
within production-grade Python applications.

### Case 1: Dynamically Shifting to Production Logging

If your application boots up in a production environment, you can dynamically switch the entire 
exception formatting pipeline into highly compact, machine-readable `logfmt` streams.

```python
import os
from simplibs.exception import SimpleExceptionSettings, LOG, PRETTY

# Detect execution environment and set appropriate presentation mode
if os.getenv("ENV") == "production":
    SimpleExceptionSettings.MESSAGE_MODE = LOG
    SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH = 150
else:
    SimpleExceptionSettings.MESSAGE_MODE = PRETTY

```

### Case 2: Ignoring Application Decorators and Utilities

When wrapping database drivers or API routes in helper decorators (like `@retry` or `@validate`), 
you want the location scanner to skip these helper files and point directly to the user source lines.

```python
from simplibs.exception import SimpleExceptionSettings

# Filter out retry library files and custom decorator paths
SimpleExceptionSettings.LOCATION_BLACKLIST = (
    "utils/decorators.py",
    "libs/retry_helper",
)

```

### Case 3: Safely Resetting Configuration (Factory Reset)

When writing unit test suites or initializing distinct thread execution contexts, 
you can roll back the entire configuration state to clean baseline settings.

```python
from simplibs.exception import SimpleExceptionSettings

# Apply temporary changes inside a unit test...
SimpleExceptionSettings.GET_LOCATION = 3
SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH = 500

# Roll back all configuration fields to factory defaults and purge internal class caches
SimpleExceptionSettings.reset()

```

[🔼 Back to Top](#-simpleexceptionsettings)

---

[⬅️ Back to README](../README.md)