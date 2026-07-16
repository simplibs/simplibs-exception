# 🧩 `bool_or_exception`

**Bi-Modal Conditional Validation Utility**

---

## 🏷️ Purpose of the Utility

When building robust data validation engines, API layers, or defensive guardrails, 
developers frequently balance two distinct error-handling strategies:

* **Graceful Failure (`return_bool=True`):** 
The validator intercepts the failure and quietly returns a boolean state indicator (`False`). 
This is ideal for inline logical branching, form validation APIs, or performance-critical conditional 
* flows where allocating exceptions is computationally unnecessary.
* **Immediate Termination (`return_bool=False`):** 
The validator immediately halts execution by throwing a fully configured, rich, structured exception. 
* This is perfect for strict runtime constraints and defensive programming.

Usually, supporting both behaviors introduces repetitive, 
cluttered `if/else` control structures inside every validation function. 
The `bool_or_exception` helper abstracts this boilerplate into a single, elegant, bi-modal line of code.

---

## ⚙️ Architectural Principles

* **Zero Boilerplate:** 
Replaces nested conditional raise/return blocks with a unified, self-documenting gateway.
* **Circular Dependency Defense:** 
Leverages lazy runtime importing of `SimpleException` inside the failure branch. 
This ensures that the utility remains decoupled and never triggers package-initialization circular locks.
* **Location Trace Continuity:** 
Automatically handles relative stack-frame adjustments. 
If a developer provides a custom integer depth, the engine increments it by `+1` to bypass 
this helper's wrapper context, guaranteeing that the captured traceback location 
always points to the true user-space call-site.
* **Strict Autocomplete Contract:** 
Uses keyword-only parameters (`*`) to guarantee explicit data passing, 
preventing argument misalignment and enabling robust IDE type-reflection.

---

## 📄 Complete Function Implementation

The implementation is designed to be lightweight, safe, and computationally optimal:

```python
def bool_or_exception(
    return_bool: bool,
    *,
    message: str | None = None,
    value: Any = UNSET,
    label: str | None = None,
    expected: str | None = None,
    problem: str | tuple[str, ...] | list[str] | None = None,
    context: str | tuple[str, ...] | list[str] | None = None,
    how_to_fix: str | tuple[str, ...] | list[str] | None = None,
    error_name: str | None = None,
    exception: Exception | type[Exception] | None = None,
    get_location: bool | int | None = None,
    skip_locations: tuple[str, ...] | str | None = None,
    oneline: bool = False,
) -> Literal[False]:
    
    # 1. Short-circuit and return False if a boolean fallback is explicitly requested
    if return_bool:
        return False

    # 2. Offset explicit integer locations to account for this helper layer context
    if isinstance(get_location, int):
        get_location += 1

    # 3. Lazy-load SimpleException inside the execution block to dismantle package circular dependencies
    from ..SimpleException import SimpleException

    # 4. Fire the structured exception down the execution stream
    raise SimpleException(
        message=message,
        value=value,
        label=label,
        expected=expected,
        problem=problem,
        context=context,
        how_to_fix=how_to_fix,
        error_name=error_name,
        exception=exception,
        get_location=get_location,
        skip_locations=skip_locations,
        oneline=oneline,
    )
```

[🔼 Back to Top](#-bool_or_exception)

---

## 🔍 Practical Usage Example

Below is a comparison showing how this utility simplifies validation code.

### ❌ Without `bool_or_exception` (Repetitive Boilerplate)

```python
from simplibs.exception import SimpleException

def validate_age(age: int, *, return_bool: bool = False) -> bool:
    if age < 0:
        if return_bool:
            return False
        raise SimpleException(
            value=age,
            label="user_age",
            expected="a positive integer (>= 0)",
            problem="age cannot be negative",
            how_to_fix="Ensure the user entered a valid year of birth."
        )
    return True
```

### With `bool_or_exception` (Clean & Unified)

```python
from simplibs.exception.tools import bool_or_exception

def validate_age(age: int, *, return_bool: bool = False) -> bool:
    if age < 0:
        return bool_or_exception(
            return_bool,
            value=age,
            label="user_age",
            expected="a positive integer (>= 0)",
            problem="age cannot be negative",
            how_to_fix="Ensure the user entered a valid year of birth."
        )
    return True
```

[🔼 Back to Top](#-bool_or_exception)

---

[⬅️ Back to README](../../README.md)