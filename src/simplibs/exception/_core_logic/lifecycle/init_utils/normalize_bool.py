from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from ....protocols import SimpleExceptionDataProtocol


def normalize_bool(
    instance: "SimpleExceptionDataProtocol",
    value: Any,
    attr: str,
) -> bool:
    """
    Validates that the value is a boolean. If not, falls back to the
    class-level default for the given attribute.
    """
    return (
        value if isinstance(value, bool)
        else bool(getattr(instance.__class__, attr, False))
    )


_DESIGN_NOTES = """
# normalize_bool.py

## Purpose
A specialized normalizer dedicated exclusively to boolean configuration 
parameters (currently `oneline`). It ensures the parameter is strictly a `bool` 
or falls back to the class-level default via reflection.

## Logic
1. If the provided `value` is a valid `bool` — it is returned as-is.
2. In all other cases (e.g., `UNSET`, `None`, wrong types like `str` or `int`) — 
   it silently fetches the class-level default from the exception class.
3. The fallback value is explicitly cast to `bool(...)` as an ultimate safety 
   measure against malformed class attributes.

## Usage
Used within `SimpleException.__init__` to handle boolean flags:
```python
self.oneline = normalize_bool(self, oneline, "oneline")
"""