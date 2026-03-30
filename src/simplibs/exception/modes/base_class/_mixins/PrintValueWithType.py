from simplibs.sentinels import UNSET
# Commons
from ....core import SimpleExceptionData


# noinspection PyMethodMayBeStatic
class PrintValueWithTypeMixin:
    """Mixin for building a string representation of a value together with its type."""

    def _print_value_with_type(
        self,
        data: SimpleExceptionData,
        *,
        intro: str = "",
    ) -> str | None:
        """
        Returns a representation of the value with its type, or None if no value was provided.

        Args:
            data:  The exception data interface.
            intro: Optional prefix before the value (e.g. 'Got: ').

        Returns:
            A string in the format 'intro"value" (type)' or None.
        """
        if data.value is UNSET:
            return None
        return f"{intro}{repr(data.value)} ({type(data.value).__name__})"


_DESIGN_NOTES = """
# PrintValueWithTypeMixin

## Purpose
Builds a readable representation of the value that caused the exception —
including its type, to aid debugging.

## Output
```
# With intro:
Got: "hello" (str)

# Without intro:
42 (int)

# If value is not provided:
None
```

## Notes
- Accepts `SimpleExceptionData` — requires the presence of the `value` attribute.
- Returns `None` if `value is UNSET` — the caller decides how to handle None
  (typically by skipping that line in the output).
- Marked `# noinspection PyMethodMayBeStatic` — as a mixin method it must
  take this form even though it does not use `self`.
"""