from typing import cast, Self
from simplibs.sentinels import UNSET, UnsetType
# Commons
from ....settings import SimpleExceptionSettings as S


# noinspection PyProtectedMember
class DunderNewMixin:
    """Mixin for dynamically adding an exception type to the class ancestors at instantiation."""

    exception: type[Exception] | UnsetType

    def __new__(
        cls,
        *args,
        exception: type[Exception] | UnsetType = UNSET,
        **kwargs
    ) -> Self:
        """
        Dynamically adds an exception type to the class ancestors if one is provided.

        Args:
            exception: The exception class to be added to the ancestors,
                       or an exception instance (edge case).

        Returns:
            A new instance — either of the original class, or of a dynamically
            created class that includes the exception type in its ancestors.
        """
        # 1. Load the class-level default if no exception was passed
        if exception is UNSET:
            exception = getattr(cls, "exception", UNSET)

        # 2. Still UNSET — no exception was provided or defined on the class, proceed without one
        if exception is UNSET:
            return super().__new__(cls)

        # 3. Edge case — an instance was passed instead of a class (necessary guard before __init__)
        if isinstance(exception, Exception):
            exception = type(exception)

        # 4. The class already includes the exception type — adding it would be redundant
        if issubclass(cls, exception):
            return super().__new__(cls)

        # 5. Create the dynamic class and store it in the cache if not already present
        cache_key = (cls, exception)
        if cache_key not in S._dynamic_cls_cache:
            S._dynamic_cls_cache[cache_key] = cast(
                type[BaseException],
                type(cls.__name__, (cls, exception), {})  # type: ignore[assignment]
            )

        # 6. Return an instance of the dynamically created class from the cache
        cached_cls = S._dynamic_cls_cache[cache_key]
        return cached_cls.__new__(cached_cls)


_DESIGN_NOTES = """
# DunderNewMixin

## Purpose
Dynamically adds an exception class (`exception`) to the ancestors of an
instance at creation time — so that `isinstance(e, ValueError)` works even
when `ValueError` is not statically present in the class hierarchy.

## Why __new__ and not __init__?
The class ancestors must be set before the instance exists — `__init__` arrives
too late. `__new__` is the only place where it is possible to control which
class the instance will represent.

## Processing flow

### Step 1 — load the class-level default
If `exception` was not passed as a parameter, the class attribute `cls.exception`
is tried as a fallback. This allows a default exception type to be declared
directly on the class:
```python
class MyError(SimpleException):
    exception = ValueError
```

### Step 2 — still UNSET after loading the default
If `exception` is still `UNSET` (not provided as a parameter and not defined
on the class), an instance of the original class is returned unchanged.

### Step 3 — edge case: instance instead of class
If the user passes an exception instance instead of a class
(`exception=ValueError()`), `__new__` silently converts it to its type.
This guard must live here — `__new__` is called before `__init__`, where
`ProcessExceptionParamMixin` would otherwise catch it. This is not a
duplication but a necessary defence at a different layer of the call stack.

### Step 4 — class already contains the exception type
If the class already has the exception type in its ancestors (for example,
the user wrote `class MyError(SimpleException, ValueError): pass` and also
passed `exception=ValueError`), adding it would create an unnecessary dynamic
class. `issubclass` detects this and returns an instance of the original class.

### Step 5 — cache
Creating dynamic classes on every call would be expensive. The created class
is therefore stored in `S._dynamic_cls_cache` under the key `(cls, exception)`.
On subsequent calls with the same combination, the class is simply retrieved
from the cache.

The cache lives in `SimpleExceptionSettings` — shared across the entire
ecosystem and included in `reset()`. Defining it directly on the mixin would
prevent a central reset and create cross-dependencies. The underscore prefix
`_dynamic_cls_cache` signals that this is not a configuration item but internal
state that settings merely hosts.

#### Why # type: ignore[assignment] is here
PyCharm still sees the type of `exception` at this point as
`type[Exception] | UnsetType` — a union that includes `UnsetType`.
The warning is technically correct from a static analysis perspective, but
factually imprecise: steps 2 and 3 have already guaranteed that `exception`
is always `type[Exception]` at this point. The type checker cannot see this
invariant because it tracks the type of a variable from its declaration, not
from the last point where it was verified. `# type: ignore[assignment]`
suppresses the warning without changing the logic — the code is correct, the
type checker simply lacks enough information to confirm it.

### Step 6 — return an instance from the cache
`super().__new__(cached_cls)` creates an instance of the dynamically assembled
class. The cache is always used — it either already contains the class (step 5
was skipped) or holds the one just created.

## Notes
- `# noinspection PyProtectedMember` is here due to access to
  `S._dynamic_cls_cache` — the underscore signals internal settings state,
  not a truly private attribute. The access is intentional and legitimate.
- The dynamic class retains the same `__name__` as the original class —
  debugging remains straightforward.
- The `isinstance` check on the exception is necessary — calling `issubclass`
  on an instance would raise a `TypeError`.
"""