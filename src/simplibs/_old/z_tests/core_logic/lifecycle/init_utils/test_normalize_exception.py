from typing import TYPE_CHECKING, Any
from inspect import isclass
# Annotations
if TYPE_CHECKING:
    from ....protocols import SimpleExceptionDataProtocol


def normalize_exception(
    instance: "SimpleExceptionDataProtocol",
    value: Any,
    attr: str = "exception"
) -> Any:
    """
    Validates that the value is either an exception instance or an exception class.
    Falls back to the class-level default if invalid.
    """
    # 1. Scénář: Je to instance výjimky (např. passed z 'except Exception as e')
    if isinstance(value, Exception):
        return value

    # 2. Scénář: Je to třída výjimky (např. exception=ValueError)
    if isclass(value) and issubclass(value, Exception):
        return value

    # 3. Fallback: Cokoliv jiného (UNSET, string, int...) vrátí default z třídy
    return getattr(instance.__class__, attr, None)


_DESIGN_NOTES = """
# normalize_exception

## Purpose
A specialized normalizer dedicated to the `exception` parameter. It ensures 
that the input is either a valid exception instance or an exception class, 
gracefully falling back to the class-level default if the input is malformed or missing.

## Logic
1. **Exception Instance Check** — If the `value` is an active instance of `Exception` 
   (e.g., caught via `except Exception as e:` and passed down), it is returned as-is.
2. **Exception Class Check** — If the `value` is a class type that inherits from 
   `Exception` (e.g., `exception=ValueError`), it is validated via `issubclass` and returned.
3. **Fallback Phase** — If the input is `UNSET`, `None`, or an invalid type (like a `str` 
   or `int`), the function silently falls back to the class-level default via reflection.

## Defensive Architecture
Like all other normalizers in `init_utils`, this function is entirely passive and 
guaranteed never to raise an internal exception. If a developer mistakenly passes 
an invalid object into the `exception` parameter, the library swallows the error 
and falls back to the default state to prevent secondary runtime crashes during 
exception instantiation.

## Where do the defaults come from?
- `SimpleExceptionData` — provides the base fallback (`None`).
- Custom Subclasses — if a developer creates a specialized domain exception and 
  defines a class-level default (e.g., `exception = ValidationError`), that specific 
  class type is dynamically fetched via `getattr` and applied.

## Usage
Used exclusively within `SimpleException.__init__` to bind the underlying cause:
```python
self.exception = normalize_exception(self, exception, "exception")
"""