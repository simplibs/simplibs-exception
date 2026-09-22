# 🧩 `build_validation_error`

**Diagnostic Factory for Failed Callable-Based Validation Rules**

---

## 🏷️ Purpose of the Utility

When validation runs through a user-supplied ad-hoc rule — a `lambda`, a plain function, or any
callable object returning `bool` — there is no class available with a predefined error message,
unlike built-in rules derived from `Rule`, which define their own `expected`/`problem`/`how_to_fix`
text via a `build_exception()` method.

`build_validation_error` fills this gap: it inspects the failing callable, extracts its name, and
assembles a fully structured `ValidationError` on its behalf — without the caller having to hand-write
the same diagnostic fields every time a callable-based rule fails.

---

## ⚙️ Architectural Principles

* **Builder, not Raiser:** 
The function only **returns** a built exception instance; it never calls `raise` itself. This keeps
the caller's own `raise` statement as the frame the location scanner sees, so the reported error
location stays accurate without needing any offset adjustment.
* **Selective Existence:** 
Not every exception category has a builder. This one exists specifically because it encapsulates real
logic — extracting `rule.__name__` (or falling back to `str(rule)`) — rather than merely forwarding
arguments into a constructor under different names.
* **Scoped to `ValidationError`:** 
Lives alongside the `ValidationError`/`ParamError` family under `exceptions/validations_errors/builders/`
rather than in the general `tools/` package, since it is bound to one specific exception class rather
than operating on exceptions generically.

---

## 📄 Complete Function Implementation

```python
def build_validation_error(
    rule: Callable[[Any], bool],
    value: Any,
    value_name: str | None = None,
    context: str | None = None,
) -> Exception:
    """Build a structured `ValidationError` exception for a failed user function or lambda."""
    rule_name = getattr(rule, "__name__", str(rule))

    return ValidationError(
        error_name="VALIDATION_ERROR",
        label=value_name,
        expected=f"value satisfying callable condition '{rule_name}'",
        value=value,
        problem=f"Value failed validation check executed by callable '{rule_name}'.",
        context=context,
        how_to_fix=(
            f"Provide a value that evaluates to True when passed to '{rule_name}'.",
        ),
        exception=ValueError,
    )
```

[🔼 Back to Top](#-build_validation_error)

---

## 🔍 Practical Usage Example

### ❌ Without `build_validation_error` (Manual Diagnostic Assembly)

```python
from simplibs.exception.exceptions import ValidationError

def check(rule, value, value_name=None):
    if not rule(value):
        rule_name = getattr(rule, "__name__", str(rule))
        raise ValidationError(
            error_name="VALIDATION_ERROR",
            label=value_name,
            expected=f"value satisfying callable condition '{rule_name}'",
            value=value,
            problem=f"Value failed validation check executed by callable '{rule_name}'.",
            how_to_fix=(f"Provide a value that evaluates to True when passed to '{rule_name}'.",),
        )
```

### ✔️ With `build_validation_error` (One Call, Same Diagnostic Quality)

```python
from simplibs.exception.exceptions.validations_errors.builders import build_validation_error

def check(rule, value, value_name=None):
    if not rule(value):
        raise build_validation_error(rule, value, value_name)
```

[🔼 Back to Top](#-build_validation_error)

---

[⬅️ Back to README](../../README.md)