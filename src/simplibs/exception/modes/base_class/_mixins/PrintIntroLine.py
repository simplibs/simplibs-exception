# Commons
from ....core import SimpleExceptionData


# noinspection PyMethodMayBeStatic
class PrintIntroLineMixin:
    """Mixin for building the opening line of the exception output."""

    def _print_intro_line(self, data: SimpleExceptionData) -> str:
        """
        Builds the opening line containing error_name and an optional value_label.

        Args:
            data: The exception data interface.

        Returns:
            A string in the format '⚠️ ERROR_NAME: value_label'
            or '⚠️ ERROR_NAME:' if value_label is not provided.
        """
        if data.value_label:
            return f"⚠️ {data.error_name}: {data.value_label}"
        return f"⚠️ {data.error_name}:"


_DESIGN_NOTES = """
# PrintIntroLineMixin

## Purpose
Builds the opening line of the exception output — combines `error_name`
and an optional `value_label` into a single string.

## Output
```
# With value_label:
⚠️ VALIDATION ERROR: parameter age

# Without value_label:
⚠️ VALIDATION ERROR:
```

## Notes
- Accepts `SimpleExceptionData` — requires the presence of the
  `error_name` and `value_label` attributes.
- Marked `# noinspection PyMethodMayBeStatic` — as a mixin method it must
  take this form even though it does not use `self`.
"""