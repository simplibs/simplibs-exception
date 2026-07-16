# 📦 `testing/asserts/functions`

**Functional Validation Assertion Suite**

The `asserts/functions` package contains three core validation utilities designed 
for testing **functions** that:

* Accept diverse parameter structures.
* Raise targeted exceptions under negative conditions.
* Successfully process valid inputs without side effects.

These assertions serve as the fundamental functional milestones leveraged 
by higher-level test orchestrators:

* `assert_exception_function`
* `bulk_test`
* Any custom test pipeline auditing functional exception logic.

---

## 📁 Package Contents

* `assert_function_callable.py`
* `assert_function_raises.py`
* `assert_function_valid_input.py`

---

## 🧭 Core Architectural Solutions

### `assert_function_callable.py`

**Validates that the target verification object is natively callable.**

Before executing functional test logic, the framework must confirm that the target object:

* Is a function or method boundary.
* Implements `__call__` or is otherwise executable by Python's runtime interpreter.

This assertion provides:

* **Fail-fast protection:** 
Prevents confusing, low-level unhandled `TypeError: '...' object is not callable` runtime crashes.
* Clear, isolated diagnostic readouts before parameterization.

---

### `assert_function_raises.py`

**Validates negative functional boundaries — ensuring the target raises an expected exception.**

This assertion verifies:

* That invoking the function with invalid parameters successfully triggers an exception.
* That the raised exception matches the specified `exception_type` contract (if provided).
* That the exception is safely intercepted using a native `pytest.raises` guard.
* That the caught exception instance is returned to the caller, 
allowing downstream field verification (fluid API).

Supported parameter layouts (routed dynamically via `process_params`):

* Scalars
* Position-based tuples
* Trailing `Kwargs` configurations
* Raw dictionaries (safely passed as positional values)

---

### `assert_function_valid_input.py`

**Validates positive functional boundaries — ensuring the target runs successfully.**

This assertion verifies:

* That the function **runs to completion without raising any exceptions**.
* That a correct, nominal input is genuinely accepted as valid.
* That the underlying target logic is not "universally broken" 
(which would render downstream negative testing meaningless).

It leverages the identical `process_params` normalizer 
to maintain execution parity with negative test passes.

---

## 🔍 Usage Examples

### Validating that a Target is Callable

```python
assert_function_callable(subtests, my_func)
```

### Validating that a Function Raises an Exception

```python
assert_function_raises(
    subtests,
    my_func,
    invalid_params=("bad",),
    exception_type=ValueError,
)
```

### Validating that a Function Successfully Processes Valid Input

```python
assert_function_valid_input(
    subtests,
    my_func,
    valid_params=("good",),
)
```

### Using Keyword Arguments with `Kwargs`

```python
from simplibs.exception.testing.tools import Kwargs

assert_function_valid_input(
    subtests,
    my_func,
    valid_params=Kwargs(mode="safe"),
)
```

[▲ Back to Top](#-testingassertsfunctions)

---

[⬅️ Back to README_TESTING](../README_TESTING.md)  
[⬅️ Back to README](../../../README.md)