# Outers
from ...SimpleExceptionData import SimpleExceptionData


def print_intro_line(
    data: SimpleExceptionData
) -> str:
    """
    Builds the opening line containing error_name and an optional label.

    Args:
        data: The exception data interface.

    Returns:
        A string in the format '⚠️ ERROR_NAME: label'
        or '⚠️ ERROR_NAME:' if label is not provided.
    """
    if data.label:
        return f"⚠️ {data.error_name}: {data.label}"
    return f"⚠️ {data.error_name}"


_DESIGN_NOTES = """
# PrintIntroLineMixin

## Purpose
Builds the opening line of the exception output — combines `error_name`
and an optional `label` into a single string.

## Output
```
# With label:
⚠️ VALIDATION ERROR: parameter age

# Without label:
⚠️ VALIDATION ERROR:
```

## Notes
- Accepts `SimpleExceptionData` — requires the presence of the
  `error_name` and `label` attributes.
- Marked `# noinspection PyMethodMayBeStatic` — as a mixin method it must
  take this form even though it does not use `self`.
"""