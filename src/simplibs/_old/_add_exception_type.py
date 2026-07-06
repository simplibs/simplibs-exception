from typing import cast
from simplibs.sentinels import UNSET, UnsetType
# Outers
from ....SimpleExceptionSettings import SimpleExceptionSettings as S


def add_exception_type(
    cls,
    exception: type[Exception] | UnsetType = UNSET,
):
    """
    Dynamically adds an exception type to the class ancestors if one is provided.

    Args:
        cls: The target exception class blueprint acting as the primary host.
        exception: The exception class to be added to the ancestors,
                   or an exception instance (edge case).

    Returns:
        A new instance — either of the original class, or of a dynamically
        created class that includes the exception type in its ancestors.
    """
    # 1. Load the class-level default if no exception was passed
    if exception is UNSET:
        exception = getattr(cls, "exception", UNSET)

    # 2. Still UNSET or None — no exception was provided, proceed with standard allocation
    if exception is UNSET or exception is None:
        return object.__new__(cls)

    # 3. Edge case — an instance was passed instead of a class (necessary guard before __init__)
    if isinstance(exception, Exception):
        exception = type(exception)

    # 4. The class already includes the exception type — adding it would be redundant
    # noinspection PyTypeChecker
    if issubclass(cls, exception):
        # noinspection PyTypeChecker
        return object.__new__(cls)

    # 5. Create the dynamic class and store it in the cache if not already present
    cache_key = (cls, exception)
    # noinspection PyProtectedMember
    dynamic_cls_cache = S._dynamic_cls_cache
    if cache_key not in dynamic_cls_cache:
        # noinspection PyTypeChecker
        dynamic_cls_cache[cache_key] = cast(
            type[BaseException],
            type(cls.__name__, (cls, exception), {})
        )

    # 6. Return an instance of the dynamically created class from the cache
    # noinspection PyTypeChecker
    cached_cls = dynamic_cls_cache[cache_key]
    return cached_cls.__new__(cached_cls)


_DESIGN_NOTES = """
# add_exception_type

## Purpose
Dynamically injects a foreign exception class (`exception`) into the inheritance ancestors (MRO) 
of an instance at creation runtime. This guarantees that native language constructs like 
`isinstance(e, ValueError)` or `except ValueError:` will trap our exception successfully, even 
when the error class is not statically present in the initial layout blueprint hierarchy.

## Execution Phase Strategy: Why __new__ and not __init__?
The inheritance graph and ancestors of a Python object must be sealed *before* the instance is fully 
allocated in memory — by the time `__init__` executes, the object layout is fixed. The `__new__` dunder 
method is the absolute single gatekeeper capable of overriding which class representation the final 
runtime instance will embody.

## Step-by-Step Processing Architecture

### Step 1 — Class-Level Blueprint Resolution
If `exception` is not explicitly passed as an initializer parameter, the engine attempts to resolve 
a default via `cls.exception`. This enables clean, declarative static class definitions:
```python
class MyCustomDatabaseError(SimpleException):
    exception = ValueError

```

### Step 2 — Empty Inheritance Fallback

If the exception reference remains completely unresolved (`UNSET` across both parameters and class states),
the lifecycle fast-paths out, returning a primitive, unmodified instance of the baseline target class.

### Step 3 — Defensive Instance Flattening

If an external consumer accidentally feeds an active instance state instead of a blueprint class
(e.g., `exception=ValueError("fault")`), the entry point flattens it to its root class type. This guard
must be evaluated here because `__new__` precedes `__init__` parameter normalizers, shielding downstream
utilities from uninstantiated metadata structures.

### Step 4 — Redundancy and Circular Inheritance Guards

If the active class structure already encapsulates the target exception inside its inheritance ancestors
(e.g., a hardcoded multi-inheritance layout like `class Custom(SimpleException, ValueError)` combined with
an explicit parameter request), adding it again would break the MRO chain. `issubclass` intercepts this and
returns a safe primitive blueprint instance.

### Step 5 — High-Performance Class Memory Cache

Spawning dynamic Python classes via `type()` on every single exception emission would leak descriptors and
severely degrade CPU performance. The engine mitigates this via an isolated storage state `S._dynamic_cls_cache`
keyed precisely against the tuple `(cls, exception)`.

* **Note on PyCharm Key Warning**: The static type inspector raises a warning regarding unhashable keys. This is a
false positive stemming from type-widening analysis tracking `UnsetType`. The upstream guards (Steps 2 & 3)
mathematically prove that `exception` is always a valid, hashable class type object at this point. The warning
is safely muted via `# noinspection PyTypeChecker`.
* **Centralized Lifecycles**: The cache database is hosted inside `SimpleExceptionSettings` to allow broad system
resets via `reset()`, treating the structural store as state-driven architecture.

### Step 6 — Instantiation Allocation

`cached_cls.__new__(cached_cls)` allocates the finalized, multi-inheritance runtime state. The compiled dynamic
class perfectly mirrors the `__name__` of the original host blueprint class, ensuring tracebacks and debuggers
remain completely intuitive to parse.
"""