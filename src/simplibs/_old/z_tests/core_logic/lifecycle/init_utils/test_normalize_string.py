from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from ....protocols import SimpleExceptionDataProtocol


def normalize_string(
    instance: "SimpleExceptionDataProtocol",
    value: Any,
    attr: str,
) -> Any:
    """
    Validates that the value is a string. If not, falls back to the
    class-level default for the given attribute.
    """
    return (
        value if isinstance(value, str)
        else getattr(instance.__class__, attr, None)
    )


_DESIGN_NOTES = """
# normalize_string

## Purpose
A specialized, high-intent normalizer dedicated exclusively to basic string 
parameters (`error_name`, `label`, `expected`, `message`). It ensures they 
are strictly bound as strings or gracefully fall back to their class-level defaults.

## Architectural Intent (Why specialized functions?)
Moving away from a generic `normalize(self, value, attr, type)` function to 
explicitly named ones (`normalize_string`, `normalize_bool`) removes type-argument 
clutter from `SimpleException.__init__`. This micro-refactoring trades a small, 
controlled duplication in helper internals for maximum readability and declarative 
intent at the call site.

## Logic
1. If the provided `value` is a valid `str` — it is returned as-is.
2. In all other cases (e.g., `UNSET`, `None`, wrong types like `int`) — it silently 
   falls back to the class-level default defined on the exception class via reflection.

## Typing & Return Value (Why 'Any'?)
The return type of this function is intentionally annotated as `Any` rather than 
`str | None`. This is a deliberate design decision to satisfy static analysis 
tools like PyCharm's Type Checker regarding strict attributes.

While fields like `label` or `message` are typed as `str | None`, the core field 
`error_name` is typed strictly as a non-nullable `str` (with a class-level default 
of `"ERROR"`). If this normalizer returned a rigid `str | None`, the IDE would raise 
a false-positive warning during assignment (`self.error_name = ...`), fearing that 
`None` might be assigned to a strict string. 

Using `Any` signals to the static analyzer that the return type dynamically 
adapts and strictly matches whichever field signature it is being assigned to via 
reflection, bypassing the rigid union type checking at the call site.

## Why a class-level default and not an exception?
In line with the defensive architecture of this library, normalizers must never 
raise an internal exception during the sanitization phase. If a user provides 
malformed metadata (e.g., `error_name=123`), the library prefers to maintain 
stability and render a standard exception layout rather than crashing the runtime 
with a secondary `TypeError`.

## Where do the defaults come from?
- `SimpleExceptionData` — provides the base fallback values for all fields.
- Custom Subclasses — if a developer creates a custom exception and overrides 
  a class attribute (e.g., `error_name = "VALIDATION_ERROR"`), that customized 
  string is dynamically fetched and used as the fallback.

## Usage
Used exclusively for string-based fields within `SimpleException.__init__`:
```python
self.error_name = normalize_string(self, error_name, "error_name")
self.label = normalize_string(self, label, "label")
self.expected = normalize_string(self, expected, "expected")
self.message = normalize_string(self, message, "message")
"""