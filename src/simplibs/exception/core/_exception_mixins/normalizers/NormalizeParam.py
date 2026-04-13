from typing import Any


class NormalizeParamMixin:
    """Mixin for normalising simple parameters based on a type check."""

    def _normalize_param(
        self,
        value: Any,
        attr: str,
        typ: type,
    ) -> Any:
        """
        Returns value if it matches the expected type, otherwise the class-level
        default for the given attribute.

        Args:
            value: The parameter value to check.
            attr:  The attribute name whose class-level default is used as the fallback.
            typ:   The expected type of the value.

        Returns:
            value if isinstance(value, typ), otherwise getattr(cls, attr).
        """
        return (
            value if isinstance(value, typ)
            else getattr(self.__class__, attr)
        )


_DESIGN_NOTES = """
# NormalizeParamMixin

## Purpose
Normalises basic parameters with a simple type (no nested or parameterised types).

## Logic
If the provided value does not match the expected type, the class-level default
defined on `SimpleExceptionData` is used in its place.

## Why a class-level default and not an exception?
The method is deliberately designed to never raise an exception.
During exception processing, no further internal errors should occur —
therefore all unsuitable inputs (including `UNSET`) are silently ignored
and replaced with the default value.

## Where do the defaults come from?
- From `SimpleExceptionData` — the base defaults for all parameters.
- If the user defined a custom class by inheriting from `SimpleException`
  and overrode class-level attributes, their values are used instead.

## Example flow
```
raise SimpleException(error_name=42)
→ isinstance(42, str) → False
→ getattr(cls, "error_name") → "ERROR"
```

## Notes
- Intended for types without nested values only (str, int, bool, etc.).
"""