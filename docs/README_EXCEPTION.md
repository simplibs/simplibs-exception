# 🧠 `SimpleException`

**The Active Execution Engine, Dynamic Inheritance, and Exception Lifecycle**

The `SimpleException` class is the primary, executable component of the entire error framework. 
While `SimpleExceptionData` acts as a passive data model, `SimpleException` represents the active runtime engine. 
It merges the pure data state with the native control-flow capabilities of Python's built-in `Exception`, 
orchestrates dynamic multiple inheritance (MRO) mutation, performs subclass safety audits during module import, 
and compiles the final visual layout representation of the error.

> 💡 **Table of Contents:**
> * [🔄 Lifecycle and Initialization Process](#-lifecycle-and-initialization-process)
> * [⚙️ Attribute Normalization in **init**](#-attribute-normalization-in-__init__)
> * [🧩 Dynamic Foreign Type Injection (MRO Mutation)](#-dynamic-foreign-type-injection-mro-mutation)
> * [🛡️ Static Subclass Contract Verification (**init_subclass**)](#-static-subclass-contract-verification-__init_subclass__)
> * [📍 Traceback Shifts and Transformations (with_location_offset)](#-traceback-shifts-and-transformations-with_location_offset)
> * [🔌 Magic Dunder Methods](#-magic-dunder-methods)

---

## 🔄 Lifecycle and Initialization Process

Creating a `SimpleException` instance involves a strict validation, sanitization, and normalization phase. 
Standard Python `dataclasses` automatically generate an `__init__` method that resets class-level overrides 
back to default states. To protect developer settings, `SimpleException` overrides this behavior entirely 
and drives its own custom initialization pipeline:

```
[User raises SimpleException]
             │
             ▼
     1. __new__(cls) ──► Calls add_exception_type() (Resolves MRO & dynamic inheritance)
             │
             ▼
     2. __init__(self)
             │
             ├──► 2.1 Parameter normalization (string, bool, exception)
             │
             ├──► 2.2 Parse skip_locations (Merges local, global, and system blacklists)
             │
             ├──► 2.3 Visual compilation (assemble_message -> dispatches to active ModeBase)
             │
             ▼
     3. Exception.__init__(self, rendered_message) (Binds finalized text to interpreter core)

```

[🔼 Back to Top](#-simpleexception)

---

## ⚙️ Attribute Normalization in `__init__`

Upon entering the constructor, all incoming arguments are processed by highly specialized sanitization functions 
to guarantee type safety and runtime predictability:

* **`normalize_string` & `normalize_bool`:** 
Validate whether the passed argument matches the expected primitive type (`str` or `bool`). 
If the verification fails or an invalid argument is supplied, they fall back 
safely to the default class-level attribute value.
* **`normalize_strings` (For `problem`, `context`, `how_to_fix`):**  
Accepts a raw string or a collection (`list`, `tuple`). 
It filters out empty strings and non-string types.  
**Optimization:** If the cleaned collection contains only a single line, 
it automatically flattens it to a plain `str`. If it contains multiple lines, 
it returns them as a sanitized `tuple[str, ...]`.
* **`normalize_exception`:** 
Verifies whether the `exception` parameter is an active exception instance 
(e.g., captured via `except Exception as e`) or an exception class reference (e.g., `ValueError`). 
Any unmapped payload types are replaced with the class-level default.
* **`process_skip_locations`:** 
Ensures that local workspace patterns ignored during a specific raise do not override global settings. 
It sequentially merges: the local override patterns + `SimpleExceptionSettings.LOCATION_BLACKLIST` + 
`SimpleExceptionSettings._SYSTEM_BLACKLIST` to produce the final, merged traceback blacklist.
* **`assemble_message` (Message Assembly):** 
Evaluates the `oneline` formatting flag. If active, it instantly forces a flattened visual layout 
via the `ONELINE` presentation mode. Otherwise, it delegates message compilation 
to the globally configured layout engine in `SimpleExceptionSettings.MESSAGE_MODE`. 
The resulting visual block is written to `self.rendered_message` and bound directly 
to the native `Exception.__init__` constructor.

[🔼 Back to Top](#-simpleexception)

---

## 🧩 Dynamic Foreign Type Injection (MRO Mutation)

One of the most powerful architectural features of `SimpleException` is its ability 
to **dynamically mutate its own Method Resolution Order (MRO)** at runtime. 
This process is driven by the `add_exception_type` utility during the `__new__` allocation phase.

### ❓ Why Is This Necessary?

When integrating this library into an existing codebase, or when catching a third-party error 
(such as `requests.exceptions.HTTPError` or Python's built-in `ValueError`), 
you want to raise a beautifully formatted `SimpleException` while preserving the ability 
for upstream error-handling blocks to intercept it using the original exception class.

### 🛠️ Under the Hood Mechanics

When a developer passes a foreign exception class or instance through the `exception` argument, 
the system performs the following steps:

1. **Defensive Instantiation Flattening:** 
If an active exception instance is passed, the engine extracts its underlying class type (`type(exception)`).
2. **Redundancy Guard:** 
If the dynamic target is already a subclass of the exception type (verified via `issubclass`), 
the mutation is bypassed.
3. **Synthetic Class Generation:** 
Utilizing Python's low-level `type(name, bases, dict)` constructor, the engine spawns a new, 
runtime-synthetic hybrid class that inherits from both your `SimpleException` subclass 
and the foreign exception class.
4. **High-Performance Memory Caching:** 
Spawning runtime types is computationally expensive. To eliminate CPU overhead, the engine caches 
these dynamic classes inside a private dictionary cache (`_dynamic_cls_cache`) in settings. 
Subsequent instantiation of identical MRO combinations resolves instantly.

```python
try:
    int("non_numeric_text")
except ValueError as err:
    # 1. Spawns a dynamic runtime hybrid (SimpleException + ValueError)
    # 2. Raises the hybrid instance
    raise SimpleException("Failed to convert value", exception=err)

# --- Upstream in your application ---
except ValueError:
    # This block successfully intercepts our SimpleException!
    # Python's native isinstance(error, ValueError) evaluates to True.
```

[🔼 Back to Top](#-simpleexception)

---

## 🛡️ Static Subclass Contract Verification (`__init_subclass__`)

When writing domain-specific custom exceptions (e.g., `class DatabaseConnectionError(SimpleException)`), 
developers can easily make typos when defining class-level configuration variables. 
Standard Python classes only surface these errors when the specific line of code is evaluated at runtime.

`SimpleException` intercepts this by overriding the `__init_subclass__` hook. 
It executes the `check_children_attributes` audit **at module import time (class definition time)**. 
If a developer defines an invalid sub-exception class, the application will refuse to start, 
throwing an early exception with precise remediation steps.

### 🔍 Import-Time Class Audits

1. **Anti-Typo Guard (Strict Whitelisting):** 
Compares all public attributes defined on the subclass against the known annotations 
in the parent `SimpleExceptionData`. If the subclass introduces an unrecognized attribute 
(e.g., writing `contextt = ...` instead of `context = ...`), the system halts with an error 
showing the list of permitted attributes and identifying missing items.
2. **Strict Default Value Type Checking:** 
Every class-level default value defined on a subclass must strictly match the type annotations 
of the parent class. This check is processed by a recursive evaluator named `_type_matches`, which:
   * Natively supports complex type unions (e.g., `str | UnsetType` or `str | tuple[str, ...] | None`).
   * Handles parameterized generics (e.g., `tuple[str, ...]`) by validating the value against 
   the origin container class (`tuple`).
   * Respects `Any` as an absolute match.



If a type mismatch is detected, the framework raises a `SimpleExceptionInternalError` 
detailing the offending attribute, the invalid type passed, the expected type constraint, 
and clear instructions on how to resolve the mismatch.

[🔼 Back to Top](#-simpleexception)

---

## 📍 Traceback Shifts and Transformations (`with_location_offset`)

In modular codebases, middleware layers, or API router frameworks, you frequently capture 
an exception in one context and re-raise it in another. If you re-raise the exception directly, 
the location-tracking engine points to your internal middleware wrapper, 
which is unhelpful to application-level developers.

The `with_location_offset(offset=1)` method resolves this by shifting the filesystem lookup 
scanner deeper down the active execution stack.

### 🔬 Offset Calculation and Immutability

To prevent side effects and keep exception states predictable, `with_location_offset` 
does not mutate the active exception instance. Instead, it instantiates a clean, 
identical clone with an adjusted `get_location` depth:

* **If `get_location` is disabled (`False`):** 
It remains strictly `False`. Shifting is ignored because stack tracing has been explicitly disabled.
* **If `get_location` is enabled as a default boolean flag (`True` or `1`):** 
The offset is added directly to the baseline: $\text{new\_depth} = 1 + \text{offset}$.
* **If `get_location` is set to a custom integer depth:** 
A standard arithmetic adjustment is applied: $\text{new\_depth} = \text{current\_depth} + \text{offset}$.

### 📖 Practical Example: Database Middleware Wrapper

```python
def safe_db_execute(query):
    try:
        return db.execute(query)
    except DatabaseError as err:
        # We want to raise our custom error, but point to where safe_db_execute was called!
        exc = SimpleException("Database transaction failed", exception=err)
        
        # Shift the stack trace analyzer 1 frame deeper to bypass this wrapper function
        raise exc.with_location_offset(1)
```

Upon creation, the cloned exception executes the stack scanning engine at the modified frame depth, 
captures the real caller's source file and line, and completely re-compiles 
its visual terminal presentation layout.

[🔼 Back to Top](#-simpleexception)

---

## 🔌 Magic Dunder Methods

To ensure seamless integration with standard Python logging frameworks, 
consoles, and testing utilities, `SimpleException` implements several key magic methods:

### `__str__(self) -> str`

Returns the compiled, formatted visual text layout block (`self.rendered_message`). 
When the interpreter, testing framework, or log aggregator prints the exception, 
the beautifully formatted terminal panel or compact log line displays naturally.

### `__repr__(self) -> str`

Returns an unambiguous engineering signature containing the precise class name and the category key:

```python
repr(error)  # Returns: <DatabaseConnectionError(error_name='DB_CONNECTION_FAILED')>
```

Because it dynamically reads `self.__class__.__name__`, it displays the correct class names 
even when inspecting synthetic, runtime-generated MRO hybrid classes (e.g., `SimpleException_ValueError`).

[🔼 Back to Top](#-simpleexception)

---

[⬅️ Back to README](../README.md)