# 🧩 `maybe_subtest`

**Conditional Context Manager**

## 🏷️ Purpose of the Utility

When building robust testing architectures, we often need to support two distinct operational execution paths:

* **Verbose Mode (`verbose=True`):** 
Every individual verification step and assertion runs inside an isolated subtest frame (`pytest-subtests`). 
If one checkpoint fails, the master test loop continues executing to evaluate 
and report on the remaining checks.
* **Silent Mode (`verbose=False`):** 
The entire sequence runs directly on the native main execution thread without subtest boundaries. 
It operates at maximum engine speed (ideal for continuous integration pipelines) 
and fails fast on the very first assertion error.

Standard implementations of this pattern lead to cluttered conditional branching 
using repetitive `if verbose: with subtests.test(...):` boilerplate. 
The `maybe_subtest` utility completely abstracts this complexity beneath 
the hood of an elegant, bi-modal context manager.

---

## ⚙️ Architectural Principles

* **Zero Syntax Pollution:** 
Eliminates duplicate branching and nested `if/else` control structures from test files.
* **Null-Object Pattern (Bi-modal Routing):** 
Acts as an intelligent runtime switch. It either mounts the runtime sequence inside Pytest's 
tracking frame or translates into an "invisible" zero-overhead passthrough generator (yielding `None`).
* **Resource Safety:** 
Leveraging an explicit `@contextmanager` generator guarantees that subtest boundaries are always safely closed, 
protecting the testing engine against trace leak configurations even during unexpected system crashes.

---

## 📄 Complete Function Implementation

By harnessing the power of Python’s standard library and `@contextmanager`, 
the implementation remains exceptionally clean and elegant:

```python
from contextlib import contextmanager
from typing import Any, Iterator

@contextmanager
def maybe_subtest(
    subtests: Any,
    *,
    name: str,
    verbose: bool,
) -> Iterator[Any]:
    """Conditionally allocate an isolated pytest subtest execution boundary.
    
    Implements a conditional Null-Object pattern for context managers. In silent mode
    (verbose=False), it falls back into a zero-overhead passthrough generator, while
    in verbose mode, it safely isolates the execution block.
    """
    if verbose:
        # Scenario 1: Active proxy gateway with isolated pytest subtest tracing
        with subtests.test(name) as ctx:
            yield ctx
    else:
        # Scenario 2: High-speed direct passthrough without subtest allocation
        yield None
```

---

## 🔍 Practical Usage Example

This context manager is highly versatile. 
You can leverage it seamlessly inside your custom assertion methods and domain validators:

```python
from simplibs.exception.testing.tools import maybe_subtest

def verify_user_profile(subtests, user, *, verbose: bool = True):
    """Custom complex audit of a user profile entity."""
    
    # Step 1: Email verification
    with maybe_subtest(subtests, name="check_email_format", verbose=verbose):
        assert "@" in user.email
        assert user.email.endswith(".cz")

    # Step 2: Age restriction check
    with maybe_subtest(subtests, name="check_age_limit", verbose=verbose):
        assert user.age >= 18

    # Step 3: Account status check
    with maybe_subtest(subtests, name="check_active_status", verbose=verbose):
        assert user.is_active is True
```

## 📊 Console Output Comparison

* **With `verbose=True` (Detailed Multi-Point Tracing):**
Pytest breaks down each validation checkpoint into its own sub-block. 
If the age check fails, the test suite continues running to verify the user status.

```text
test_users.py::test_user_registration SUBPASSED [check_email_format]
test_users.py::test_user_registration SUBPASSED [check_age_limit]
test_users.py::test_user_registration SUBPASSED [check_active_status]
```

* **With `verbose=False` (Fast Continuous Integration Pass):**
All checkpoints execute directly on the native main execution path with zero subtest allocation overhead. 
Any failure immediately stops the entire test.

```text
test_users.py::test_user_registration PASSED
```

[▲ Back to Top](#-maybe_subtest)

---

[⬅️ Back to README_TESTING](../README_TESTING.md)  
[⬅️ Back to README](../../../README.md)