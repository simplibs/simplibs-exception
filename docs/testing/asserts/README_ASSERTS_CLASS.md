# 📦 `testing/asserts/classes`

**Exception Class Structural Validation Suite**

The `asserts/classes` package contains four core validation utilities 
that together establish a comprehensive testing pipeline for auditing the **structure**, 
**default fallback states**, **constructor propagation**, 
and the **public API** of custom **SimpleException** classes.

These assertions serve as the fundamental structural milestones leveraged 
by the higher-level test orchestrators:

* `assert_exception_class`
* `assert_exception_function`
* `bulk_test`

Each assertion targets a single, strictly defined architectural boundary — combined, 
they form a complete diagnostic audit suite for any framework-compliant exception.

---

## 📁 Package Contents

* `assert_class_inheritance.py`
* `assert_class_defaults.py`
* `assert_class_constructor.py`
* `assert_class_interface.py`

---

## 🧭 Core Architectural Solutions

### `assert_class_inheritance.py`

**Validates the underlying class type hierarchy of the exception.**

Every custom exception must satisfy mandatory architectural inheritance constraints:

* It must derive from `BaseException`.
* It must derive from `SimpleExceptionData`.
* It must optionally derive from any additional custom polymorphic parents supplied 
via the `expected_parents` parameter.

This assertion guarantees:

* **Fail-fast behavior:** 
If `BaseException` is missing, execution halts immediately before triggering unpredictable downstream errors.
* That the exception properly incorporates the core framework telemetry and data layout layer.
* That the class is natively recognized by the Python runtime 
as an escapable error blueprint that can be triggered via `raise`.

---

### `assert_class_defaults.py`

**Validates class-level default metadata and its propagation to the instance.**

Every custom exception class defines fallback metadata directly on its class body level:

```python
class MyError(SimpleExceptionData, Exception):
    error_name = "MY_ERROR"
    label = "core"

```

This assertion verifies:

* That an instance initialized without constructor arguments correctly inherits 
and preserves the static class-level values.
* That the constructor doesn’t mutate or wipe out the defined fallback properties.
* That the exception behaves deterministically and remains pure out-of-the-box.

By using reflection via `exc_class.__dict__`, this engine isolates 
and tests **exclusively attributes declared directly on the class body level**.

---

### `assert_class_constructor.py`

**Validates the state initialization boundaries and argument mapping of the constructor.**

Every custom exception must safely accept and map the complete set of framework-supported telemetry fields:

* `message`
* `value`
* `label`
* `expected`
* `problem`
* `context`
* `how_to_fix`
* `error_name`
* `exception`
* `get_location`
* `skip_locations`
* `oneline`

This assertion:

* Instantiates the exception with a complete, unique reference matrix.
* Verifies that the resulting instance layout perfectly mirrors the original reference data.
* Instantly exposes any argument mutation, data loss, or missing bindings inside the custom constructor.

---

### `assert_class_interface.py`

**Validates compliance of the exception's public API (string formatting and data serialization).**

Every custom exception must fully expose and execute the required dunder formatting methods 
and serialization channels:

* `__str__()`
* `__repr__()`
* `to_dict()`
* `to_debug_dict()`
* `to_json()`

This assertion verifies:

* That all required API methods are defined and callable.
* That they return the correct data types (`str`, `dict`, `str`).
* That the exception is fully compatible with terminal loggers, print routines, and automated storage dumpers.

---

## 🔍 Usage Examples

### Complete Audit of an Exception Class

```python
from simplibs.exception.testing.assert_exception_class import assert_exception_class

def test_my_error(subtests):
    assert_exception_class(subtests, MyError)
```

### Isolating Defaults Verification

```python
assert_class_defaults(subtests, MyError)
```

### Isolating Constructor Mapping Verification

```python
assert_class_constructor(subtests, MyError)
```

### Isolating Public API Type Compliance Verification

```python
assert_class_interface(subtests, MyError)
```

### Isolating Hierarchy Contract Verification

```python
assert_class_inheritance(subtests, MyError)
```

[▲ Back to Top](#-testingassertsclasses)

---

[⬅️ Back to README_TESTING](../README_TESTING.md)  
[⬅️ Back to README](../../../README.md)
