from dataclasses import dataclass
# Commons
from ..data import SimpleExceptionData


@dataclass
class SimpleExceptionInternalError(SimpleExceptionData, Exception):
    """Internal library exception — no validation, direct output only."""


    # Available attributes:
    error_name: str = "INTERNAL ERROR"
    # value: object = UNSET
    # value_label: str = UNSET
    # expected: str = UNSET
    # problem: str = UNSET
    # context: str = UNSET
    # how_to_fix: tuple[str, ...] = UNSET


    # Build the message:
    def __post_init__(self):

        # 1. Render the message
        from ...modes import PRETTY
        rendered_message = PRETTY(self, validate=False)

        # 2. Pass the message to the exception
        # Instead of super().__init__ we write directly to Exception.args —
        # this ensures Exception(message) works correctly without overwriting our data.
        Exception.__init__(self, rendered_message)


_DESIGN_NOTES = """
# SimpleExceptionInternalError

## Purpose
The base internal exception of the library — completely isolated from
`SimpleException` logic. Inherits directly from `SimpleExceptionData`
and `Exception`, with no dependency on the rest of the library beyond
the `PRETTY` mode.

## Isolation and lazy import
`PRETTY` is loaded lazily inside `__post_init__` to avoid a circular import —
`SimpleExceptionInternalError` lives in `core/_internal_exception` and a
standard top-level import of `modes` would pull it back in. The lazy import
breaks this cycle and loads the mode only when it is actually needed.

`PRETTY` is called with `validate=False` for two reasons:
- This is an internal call where the data is already guaranteed to be correct —
  validation is unnecessary.
- Validation would re-import `modes` and cause a circular import even through
  the lazy import.

`PRETTY` is hardcoded — a deliberate choice for reliability. Internal library
exceptions must produce consistent output regardless of the active settings
configuration. In the very situations these exceptions handle (misconfiguration,
logic errors in modes) the settings may be unreliable or only partially
initialised.

## Group base class
Serves as the base for grouped internal library exceptions:
```python
class SimpleExceptionSettingsError(SimpleExceptionInternalError):
    error_name: str = "SETTINGS ERROR"
```
Grouped exceptions can be caught together:
```python
except SimpleExceptionInternalError:
    ...
```

## Attributes to define
A full description of all attributes is in `SimpleExceptionData._DESIGN_NOTES`.
For internal exceptions, only the following are typically needed:

| Attribute     | Description                                                       |
|---------------|-------------------------------------------------------------------|
| `error_name`  | Exception group name — displayed as the heading in the output     |
| `value`       | The value that caused the exception                               |
| `value_label` | Label for the value — e.g. the attribute or parameter name        |
| `expected`    | What was expected                                                 |
| `problem`     | What is wrong                                                     |
| `context`     | Additional context — only include if it adds meaningful information|
| `how_to_fix`  | Tips on how to resolve the error                                  |

## Commented-out attributes
The commented-out attributes in the class definition serve as a quick
declarative reference — without reading the documentation it is immediately
clear which attributes are meaningful to define.
"""