# 📚 `exceptions`

**The Shared, Categorized Exception Library of the `simplibs` Ecosystem**

---

## 🏷️ Purpose

Every `simplibs` library eventually needs to raise the same kinds of general-purpose errors — a bad
parameter, a missing resource, an object used before it was initialized. Without a shared place to
define these, each library ends up redefining an equivalent exception locally, with slightly different
names and slightly different shapes.

The `exceptions` package solves this by providing **one categorized, importable tree** of general
exceptions. Any `simplibs` library imports what it needs from here instead of reinventing it —
libraries only define their own exception classes for genuinely library-specific failure modes that
don't fit any category below.

```python
from simplibs.exception.exceptions import ParamError

def set_age(age: int):
    if age < 0:
        raise ParamError(label="age", expected="a non-negative integer", value=age)
```

---

## ⚙️ Construction

* **`SimpleError` as the Common Root:** 
Every class in this package inherits — directly or indirectly — from `SimpleError`, which itself
inherits from `SimpleException`. `SimpleError` is never raised directly and carries no logic; it exists
purely so code can distinguish "one of the ecosystem's categorized exceptions" from a bare
`raise SimpleException(...)` ad-hoc marker used elsewhere.
* **Category Roots + Specializations:** 
Each failure domain has one general root class (e.g. `ValidationError`, `StateError`, `ResourceError`)
and, where a common specific scenario recurs often enough, one or more subclasses of it (e.g.
`ParamError` under `ValidationError`). Raise the root only when no specialization fits.
* **Folder-per-Category:** 
Each category lives in its own sub-package (`validations_errors/`, `state_errors/`, `resource_errors/`,
`operation_errors/`, `conversion_errors/`, `dependency_errors/`), keeping related classes and their
optional builders grouped together.
* **Builders are Optional and Selective:** 
Some categories ship a `builders/` sub-package with factory functions (see
[`build_validation_error`](../tools/README_BUILD_VALIDATION_ERROR.md)) — but only where the diagnostic
message needs logic beyond rearranging constructor arguments. Most classes stay empty (`pass`) and are
raised directly.

---

## 📋 Exception Registry

| Class                 | Parent            | Description                                                                 |
| :--------------------- | :----------------- | :---------------------------------------------------------------------------- |
| `SimpleError`         | `SimpleException` | Root of all named, categorized exceptions. Never raised directly.            |
| `ValidationError`     | `SimpleError`      | A value or input failed to satisfy a required condition.                     |
| `ParamError`          | `ValidationError`  | A function or constructor parameter failed validation.                       |
| `StateError`          | `SimpleError`      | An object or system is not in the state a given operation requires.         |
| `InitializationError` | `StateError`       | An object or system was used before it was properly initialized.            |
| `ConfigurationError`  | `StateError`       | Required configuration is missing or invalid.                               |
| `ResourceError`       | `SimpleError`      | A problem occurred while working with an identifiable resource.             |
| `NotFoundError`       | `ResourceError`    | A requested resource does not exist.                                        |
| `AlreadyExistsError`  | `ResourceError`    | A resource could not be created because it already exists.                  |
| `AccessError`         | `ResourceError`    | A resource exists but cannot be accessed due to missing permissions or a lock. |
| `OperationError`      | `SimpleError`      | A runtime operation or process failed while executing.                      |
| `ConversionError`     | `SimpleError`      | A value could not be converted from one type or format to another.          |
| `DependencyError`     | `SimpleError`      | A required dependency is missing, incompatible, or failed to load.          |

---

## 🔍 Practical Usage Example

```python
from simplibs.exception.exceptions import (
    ParamError,
    NotFoundError,
    ConfigurationError,
)

def get_user(user_id: int):
    if user_id < 0:
        raise ParamError(label="user_id", expected="a non-negative integer", value=user_id)

    user = database.find(user_id)
    if user is None:
        raise NotFoundError(label="user", expected=f"a user with id {user_id}")

    return user

def load_settings(path: str):
    if not path:
        raise ConfigurationError(label="settings path", problem="no configuration path was provided")
```

[🔼 Back to Top](#-exceptions)

---

[⬅️ Back to README](../../README.md)