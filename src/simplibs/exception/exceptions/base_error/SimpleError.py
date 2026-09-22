# Inners
from ...core.SimpleException import SimpleException


class SimpleError(SimpleException):
    """Root of all named, categorized exceptions in the simplibs ecosystem.

    Unlike `SimpleException`, which can be raised directly as an ad-hoc marker
    (`raise SimpleException()`), `SimpleError` is never raised on its own.
    It exists purely as a catch-all ancestor for every structured exception
    defined under `exceptions/`, so consumers can distinguish between
    "any framework exception" and "any deliberately categorized exception".
    """
    pass


_DESIGN_NOTES = """
# SimpleError

## Purpose
Acts as the shared root for every named exception class living under
`exceptions/` (`ValidationError`, `StateError`, `ResourceError`, ...).
It carries no behavior of its own — it exists solely to give the categorized
exception tree a common ancestor distinct from `SimpleException` itself.

## Rationale
`SimpleException` is dual-purpose: it works both as an ad-hoc marker
(`raise SimpleException("something broke")`) and as the technical base class
every structured exception ultimately inherits from. Without `SimpleError`,
code that wants to catch "one of my categorized domain exceptions" has no way
to do so without also catching every unrelated ad-hoc marker raised anywhere
in foreign code that happens to use `SimpleException` directly.

```python
try:
    ...
except SimpleError:
    # Catches ParamError, StateError, ResourceError, etc. — but NOT a bare
    # `raise SimpleException("...")` used as a quick marker elsewhere.
    ...
```

## Design Constraint
`SimpleError` must never be raised directly and must never carry logic.
It is purely a structural marker in the MRO.
"""