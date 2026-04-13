from simplibs.sentinels import UNSET
# Outers
from ....core import SimpleExceptionData


# noinspection PyMethodMayBeStatic
class PrintValueWithTypeMixin:
    """Mixin for building a string representation of a value together with its type."""

    def _print_value_with_type(
        self,
        data: SimpleExceptionData,
        *,
        intro: str = "",
        max_length: int | None = None,
    ) -> str | None:
        """
        Returns a representation of the value with its type, or None if no value was provided.

        Args:
            data:       The exception data interface.
            intro:      Optional prefix before the value (e.g. 'Got: ').
            max_length: Optional manual override for truncation. If None,
                        uses settings.DEFAULT_VALUE_TRUNCATION_LENGTH.

        Returns:
            A string in the format 'intro"value" (type)' or None.
        """
        # 1. If value is not provided, return None
        if data.value is UNSET:
            return None

        # 2. Obtain string representation (repr)
        repr_str = repr(data.value)

        # 3. Use global setting if local override is not provided
        if max_length is None:
            from ....core import SimpleExceptionSettings as S
            max_length = S.DEFAULT_VALUE_TRUNCATION_LENGTH

        # 4. Truncation magic: if longer than limit, cut it and add info about hidden chars
        if len(repr_str) > max_length:
            truncated_chars = len(repr_str) - max_length
            repr_str = (
                repr_str[:max_length] +
                f"... [truncated, {truncated_chars} chars]"
            )

        # 5. Return formatted string with type information
        return f"{intro}{repr_str} ({type(data.value).__name__})"


_DESIGN_NOTES = """
# PrintValueWithTypeMixin

## Purpose
Builds a readable representation of the inspected value, including its type 
and handling potential truncation of extremely long strings.

## Truncation Logic
To prevent the exception message from being overwhelmed by large data objects 
(like massive dictionaries or long strings), the mixin automatically truncates 
the `repr()` of the value.
- **Default limit**: Controlled by `SimpleExceptionSettings.DEFAULT_VALUE_TRUNCATION_LENGTH`.
- **Manual override**: Can be specified via the `max_length` argument.
- **Feedback**: If truncated, it appends a notice with the count of hidden characters.

## Output Examples
```
# Standard:
Got: "hello" (str)

# Truncated:
Got: "very long str..." [truncated, 450 chars] (str)

# If value is UNSET:
None
```

## Integration
Like all output mixins, this one follows the unified signature: it accepts 
the `SimpleExceptionData` object. This ensures consistency across all modes 
(PRETTY, LOG, etc.) and keeps the rendering workflow predictable.

## Notes
- Returns `None` if `data.value` is `UNSET`. Callers typically use `if line: ...` 
  to skip rendering this line entirely.
- It uses `repr()` instead of `str()` to ensure that the representation 
  is unambiguous (e.g., distinguishing between `'5'` and `5`).
"""