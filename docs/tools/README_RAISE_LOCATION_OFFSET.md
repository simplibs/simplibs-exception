# 📦 `raise_location_offset`

**Declarative Stack-Frame Calibration Decorator**

---

## 🧩 Purpose of the Utility

In modular software architectures, helper validation functions, gateway assertions, 
or utility wrappers frequently perform runtime parameter checks. 
When one of these checks fails and raises an exception, the traceback naturally points 
to the line *inside* the helper function where the error was originally thrown.

To an integration developer, this internal location is unhelpful noise. 
What they actually need to see is the exact line in *their own application code* 
where they invoked your helper.

The `raise_location_offset` decorator automates this stack-frame shifting. 
By decorating your utility functions, you automatically intercept any bubbling exceptions 
and cleanly re-target them so that the terminal error report points directly to the caller.

---

## ⚙️ Architectural Principles

* **AOP-Style Decoupling:** 
Implements a declarative Aspect-Oriented Programming (AOP) wrapper. 
It cleanly isolates your core validation logic from stack-frame tracking concerns.
* **Metadata Preservation:** 
Uses `functools.wraps` to ensure the decorated function preserves its original signature, 
docstrings, name, and type annotations, keeping static analyzers and IDEs fully aligned.
* **Duck-Typed Boundary Isolation:** 
Leverages runtime duck-typing to check for `with_location_offset` on any caught exception, 
eliminating direct imports of concrete exception classes.
* **Clean Traceback Context:** 
For both custom and native Python exceptions, the decorator raises the error 
using the `raise ... from None` syntax. This prevents Python from compounding 
local decorator frame contexts, leaving you with a pristine terminal report.

---

## 📄 Complete Function Implementation

The implementation is designed to be elegant, clean, and highly resilient:

```python
def raise_location_offset(
    offset: int = 1
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator that catches an exception and adds a location offset before re-raising."""

    # 1. Define the decorator boundary layer receiving the target function blueprint
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        # 2. Define the execution wrapper conserving the original signature metadata
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            # 2.1 Enclose execution within a defensive evaluation block
            try:
                return func(*args, **kwargs)
            except Exception as e:

                # 2.2 Evaluate via runtime duck-typing whether the exception supports frame shifting
                if hasattr(e, "with_location_offset"):
                    # 2.3 Add relative offset and re-raise suppressing local execution context
                    raise e.with_location_offset(offset) from None

                # 2.4 Resilient fallback for native standard exceptions (e.g. ValueError).
                # Using 'from None' isolates the original traceback graph from being overwritten.
                raise e from None

        # Return the configured wrapper
        return wrapper

    # Return the structural decorator
    return decorator
```

[🔼 Back to Top](#-raise_location_offset)

---

## 🔍 Practical Usage Example

The following scenario illustrates how the decorator simplifies error reporting for utility functions.

### ❌ Without `raise_location_offset` (Standard Behavior)

```python
from simplibs.exception import SimpleException

def assert_positive_number(n: int):
    if n <= 0:
        raise SimpleException(
            value=n,
            label="number",
            expected="a value strictly greater than 0"
        )

# Client code (where you consume the utility)
assert_positive_number(-10)  # 💥 Traceback points to "raise SimpleException" inside the helper!
```

### ✔️ With `raise_location_offset` (Clean Caller-Site Target)

```python
from simplibs.exception import SimpleException
from simplibs.exception.tools import raise_location_offset

@raise_location_offset(offset=1)
def assert_positive_number(n: int):
    if n <= 0:
        raise SimpleException(
            value=n,
            label="number",
            expected="a value strictly greater than 0"
        )

# Client code (where you consume the utility)
assert_positive_number(-10)  # 🎉 Traceback points directly to this line!
```

[🔼 Back to Top](#-raise_location_offset)

---

[⬅️ Back to README](../../README.md)