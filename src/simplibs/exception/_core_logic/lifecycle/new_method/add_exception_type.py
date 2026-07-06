from typing import TypeVar, cast
# Outers
from ....SimpleExceptionSettings import SimpleExceptionSettings as S

T = TypeVar("T", bound=BaseException)


def add_exception_type(
    cls: type[T],
    exception: type[Exception] | Exception | None = None,
) -> type[T]:
    """
    Resolves the runtime class layout that should be instantiated.

    If an additional foreign exception type is requested, a cached dynamic subclass
    combining both inheritance trees (MRO) is returned to support native language
    constructs like isinstance() or try/except blocks. Otherwise, the original
    class blueprint is returned unchanged.

    Output Forms:
        Standard Case:
            With exception:    Returns a dynamic sub-type combining (cls, requested_exception)
            Without exception: Returns the original unmodified cls blueprint
    """
    # 1. Load the class-line default ONLY if the parameter was omitted (is None)
    if exception is None:
        exception = getattr(cls, "exception", None)

    # 2. No exception requested -> keep the original class blueprint
    if exception is None:
        return cls

    # 3. Defensive instance flattening: if an active instance was passed, extract its type
    if isinstance(exception, Exception):
        exception = type(exception)

    # 4. Circular and redundancy guard: if already inherited, nothing to do
    # noinspection PyTypeChecker
    if issubclass(cls, exception):
        return cls

    # 5. High-performance class memory cache execution
    cache_key = (cls, exception)
    # noinspection PyProtectedMember
    dynamic_cls_cache = S._dynamic_cls_cache

    if cache_key not in dynamic_cls_cache:
        # noinspection PyTypeChecker
        dynamic_cls_cache[cache_key] = cast(
            type[T],
            type(cls.__name__, (cls, exception), {})
        )

    # 6. Return the finalized runtime class from the cache
    # noinspection PyTypeChecker
    return dynamic_cls_cache[cache_key]


_DESIGN_NOTES = """
# add_exception_type

## Purpose
Resolves a dynamic class blueprint that injects a foreign exception class (`exception`) into the 
inheritance ancestors (MRO) of the targeted host class. This guarantees that native language 
constructs like `isinstance(e, ValueError)` or `except ValueError:` successfully trap the final 
instance at runtime, even when the foreign error type is not statically present in the initial class hierarchy.

## Execution Phase Strategy: Class Factory Pattern
Unlike typical `__new__` helpers that allocate memory directly, this component operates strictly as a 
Class Factory. It separates class graph generation from object instantiation. The helper returns the resolved 
class blueprint, allowing the calling context (e.g., the host's `__new__` method) to handle the 
standard instantiation process via its native inheritance path.

## Step-by-Step Processing Architecture

### Step 1 — Class-Level Blueprint Resolution
If `exception` is omitted or passed as `None`, the engine checks for a default class-level fallback 
via `cls.exception`. This enables clean, declarative static definitions:
```python
class MyCustomDatabaseError(SimpleException):
    exception = ValueError

```

### Step 2 — Original Blueprint Fallback

If no additional exception type is requested parameters-wise or defined on the class level, the engine
fast-paths out, returning the original `cls` blueprint completely unmodified.

### Step 3 — Defensive Instance Flattening

If a consumer accidentally feeds an active exception instance instead of a blueprint class
(e.g., `exception=ValueError("fault")`), the guard flattens it to its root type via `type(exception)`.
This acts as a structural shield before downstream utilities inspect the type.

### Step 4 — Redundancy and Circular Inheritance Guards

If the host class structure already encapsulates the target exception inside its inheritance ancestors
(e.g., a hardcoded multi-inheritance layout combined with an explicit runtime parameter request), adding
it again would corrupt the MRO chain. `issubclass` intercepts this and safely returns the unmodified `cls`.

### Step 5 — High-Performance Class Memory Cache

Spawning dynamic Python classes via `type()` on every single exception emission degrades CPU performance
and duplicates type generation. The engine mitigates this via a dedicated registry `S._dynamic_cls_cache`
keyed precisely against the tuple `(cls, exception)`.

* **Centralized Lifecycles**: The cache storage is hosted inside `SimpleExceptionSettings` to allow global system
flushes via `reset()`, treating the structural registry as state-driven architecture.

### Step 6 — Runtime Class Return

The engine fetches the cached dynamic type and returns it. The dynamic class perfectly mirrors the
`__name__` of the original host blueprint class, ensuring tracebacks, logging utilities, and IDE debuggers
remain completely intuitive to parse.
"""
