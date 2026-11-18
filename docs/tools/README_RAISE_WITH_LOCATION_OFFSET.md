# 🧩 `raise_with_location_offset`

**Unified Re-raising and Call-Site Calibration Utility**

---

## 🏷️ Purpose of the Utility

When managing errors across multi-layered software architectures—such as API controllers, 
database adapters, or middleware wrappers—developers frequently catch an exception 
and re-throw it to a higher application layer.

To prevent internal adapter or wrapper frames from polluting the terminal output or logs, 
the exception's target stack-trace location must be shifted deeper into the execution stack.

* **Standard Fluent Approach:** 
Requires modifying and then explicitly raising the object: `raise exc.with_location_offset(offset)`.
* **This Utility:** 
Consolidates this pattern into a single functional command pass. 
It supports both custom `SimpleException` structures and native standard Python exceptions 
under one unified interface.

---

## ⚙️ Architectural Principles

* **Explicit Duck-Typing:** 
To eliminate import-time package-dependency loops and remain completely decoupled 
from specific high-level exception class paths, the utility evaluates capabilities 
at runtime using structural duck-typing (checking for the presence of the `with_location_offset` method).
* **Resilient Standard Fallback:** 
If a native Python exception (such as `ValueError` or `KeyError`) is passed, 
the utility seamlessly degrades into a standard passthrough dispatcher, 
raising the raw error without modification.
* **Traceback Context Isolation:** 
Uses the `raise exc from None` pattern for native fallbacks. 
This prevents Python from compounding local frame mutation exception contexts, 
fully preserving the original underlying traceback graph.

---

## 📄 Complete Function Implementation

The implementation is highly robust, lightweight, and designed with defensive execution fallbacks:

```python
def raise_with_location_offset(
    exc: "BaseException | SimpleExceptionProtocol | Any",
    offset: int = 1,
) -> NoReturn:
    """Takes an exception, applies a relative stack-frame location offset if supported, and raises it."""
    # 1. Evaluate via runtime duck-typing whether the exception supports frame shifting mutation
    if hasattr(exc, "with_location_offset"):
        raise exc.with_location_offset(offset)

    # 2. Resilient fallback for standard Python exceptions (e.g. ValueError, TypeError).
    # Using 'from None' prevents Python from compounding a local frame mutation exception context,
    # thereby fully preserving the original underlying traceback of the raw exception object.
    raise exc from None
```

[🔼 Back to Top](#-raise_with_location_offset)

---

## 🔍 Practical Usage Example

Below is a comparison demonstrating how this utility simplifies error-propagation blocks.

### ❌ Without `raise_with_location_offset` (Two-Step Manual Invocation)

```python
from simplibs.exception import SimpleException

def process_transaction(data):
    try:
        execute_db_query(data)
    except DatabaseConnectionError as err:
        exc = SimpleException("Database transaction failed", exception=err)
        # Requires manual instantiation modification followed by an explicit raise
        raise exc.with_location_offset(1)
```

### ✔️ With `raise_with_location_offset` (One-Line Propagation)

```python
from simplibs.exception import SimpleException
from simplibs.exception.tools import raise_with_location_offset

def process_transaction(data):
    try:
        execute_db_query(data)
    except DatabaseConnectionError as err:
        # Instantly calibrates and raises in a single operational step
        raise_with_location_offset(
            SimpleException("Database transaction failed", exception=err), 
            offset=1
        )
```

[🔼 Back to Top](#-raise_with_location_offset)

---

[⬅️ Back to README](../../README.md)