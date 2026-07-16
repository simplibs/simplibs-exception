# 🧩 `Kwargs`

**Semantic Invocation Wrapper**

## 🏷️ Purpose of the Utility

When conducting automated functional testing (such as executing matrix sweeps via `bulk_test`), 
we encounter a fundamental type ambiguity in Python. A standard dictionary `{...}` can represent either:

1. **A singular literal data value** (e.g., passing a dictionary as a single positional `value` argument).
2. **A set of named keyword parameters** (intended to be expanded into the target function signature as `kwargs`).

The `Kwargs` class acts as an explicit **semantic label (token)**. 
Wrapping your dictionary in `Kwargs` immediately and safely signals to the test orchestration pipeline 
that the encapsulated mapping structure must be expanded into named keyword parameters (`kwargs`) 
upon function invocation, rather than evaluated as a standard positional value.

---

## ⚙️ Architectural Principles

* **Ambiguity Elimination (Type Safety):** 
Eliminates the risk of the testing engine misinterpreting a test parameter mapping block as a raw data value.
* **Immutability (Side-Effect Protection):** 
The instance is completely frozen upon creation (`frozen=True` with `slots=True`). 
This guarantees that downstream test pipelines cannot accidentally mutate the parameter payload during execution.
* **Native Double-Asterisk Unpacking:** 
By fully implementing the `collections.abc.Mapping` protocol, `Kwargs` achieves native dictionary polymorphism. 
You can unpack it anywhere in Python using standard syntax: `func(Kwargs(a=1))`.
* **Guarded Initialization:** 
If an attempt is made to initialize `Kwargs` with invalid patterns 
(e.g., passing multiple positional arguments or an object that is not a subclass of `Mapping`), 
the internal validator halts execution instantly, raising a clear 
and actionable framework exception before unpredictable downstream crashes occur.

---

## 🛠️ Usage Patterns

The class inherits from `collections.abc.Mapping`, is fully **frozen**, 
and supports two secure initialization patterns:

```python
from simplibs.exception.testing.tools import Kwargs

# Pattern 1: Initialization via inline named parameters
invalid_params = Kwargs(timeout=10, strict=True)

# Pattern 2: Initialization by passing an existing dictionary mapping
invalid_params = Kwargs({"timeout": 10, "strict": True})
```

---

## 🔍 Practical Test Example

Consider a function that accepts variable keyword arguments, 
and we want to audit its failure paths. By leveraging `Kwargs`, 
we define and route the dynamic payload with absolute clarity:

```python
# The target function under test
def validate_connection(**kwargs):
    if kwargs.get("timeout", 0) > 60:
        raise SimpleExceptionSettingsError(
            value=kwargs["timeout"],
            label="timeout",
            problem="Connection timeout cannot exceed 60 seconds."
        )

# Leveraging explicit Kwargs inside a test block
def test_validate_connection(subtests):
    assert_exception_function(
        subtests,
        validate_connection,
        invalid_params=Kwargs(timeout=99, strict=True), # Safely unpacked as **kwargs
        exception_type=SimpleExceptionSettingsError,
        value=99,
        label="timeout",
        problem="Connection timeout cannot exceed 60 seconds."
    )
```

[▲ Back to Top](#-kwargs)

---

[⬅️ Back to README_TESTING](../README_TESTING.md)  
[⬅️ Back to README](../../../README.md)