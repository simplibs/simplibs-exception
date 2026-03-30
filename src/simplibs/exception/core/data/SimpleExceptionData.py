from dataclasses import dataclass
from simplibs.sentinels import UNSET, UnsetType


@dataclass
class SimpleExceptionData:
    """Data class defining the structure and default values of SimpleException."""

    # --- Core exception info ---
    error_name: str = "ERROR"
    exception: type[Exception] | UnsetType = UNSET
    _intercepted_exception: str | UnsetType = UNSET

    # --- Info about the inspected value ---
    value: object = UNSET
    value_label: str | UnsetType = UNSET

    # --- Exception description ---
    expected: str | UnsetType = UNSET
    problem: str | UnsetType = UNSET
    context: str | UnsetType = UNSET
    message: str | UnsetType = UNSET

    # --- How to fix ---
    how_to_fix: tuple[str, ...] | UnsetType = UNSET

    # --- Location info ---
    _get_location: int | bool = True
    _skip_locations: tuple[str, ...] = ()

    # --- Single-line output ---
    _oneline: bool = False


_DESIGN_NOTES = """
# SimpleExceptionData

## Purpose
A data class defining the structure, default values, and interface of `SimpleException`.
Completely isolated from the rest of the library — it has no dependencies on
`SimpleExceptionSettings` or any other library class. This makes it a shared
foundation for:

1. **`SimpleException`** — subclasses can override public attributes
   to change default behaviour.
2. **Internal exceptions** — `SimpleExceptionInternalError` and its subclasses
   share the same structure without depending on `SimpleException` logic.
3. **Data protocol for modes** — `ModeBase` expects data with this structure.
   Custom modes can optionally validate input via `validate=True`.

## Underscore convention
- **Without underscore** — input parameters that the user can set either as
  `__init__` arguments or as class-level attributes on subclasses.
- **With underscore** (`_intercepted_exception`, `_get_location`, etc.) —
  values that are computed or managed automatically by the system.
  The user should never set these directly.

## Attribute reference

### Core info
| Attribute               | Default   | Description                                          |
|-------------------------|-----------|------------------------------------------------------|
| `error_name`            | `"ERROR"` | Error name displayed in the exception output         |
| `exception`             | `UNSET`   | Exception class dynamically added to the MRO         |
| `_intercepted_exception`| `UNSET`   | Description of a caught exception — set automatically|

### Inspected value
| Attribute     | Default | Description                                               |
|---------------|---------|-----------------------------------------------------------|
| `value`       | `UNSET` | The value that caused the exception                       |
| `value_label` | `UNSET` | Human-readable label for the value (e.g. `"parameter age"`) |

### Exception description
| Attribute  | Default | Description                                                      |
|------------|---------|------------------------------------------------------------------|
| `expected` | `UNSET` | What was expected (e.g. `"a positive integer"`)                  |
| `problem`  | `UNSET` | What is wrong (e.g. `"value is negative"`)                       |
| `context`  | `UNSET` | Broader context — only include if it adds meaningful information  |
| `message`  | `UNSET` | Free-form message — an alternative to the structured parameters  |

### Location
| Attribute         | Default | Description                                                         |
|-------------------|---------|---------------------------------------------------------------------|
| `_get_location`   | `True`  | Enable/disable location reporting, or set stack depth               |
| `_skip_locations` | `()`    | Strings matched against file paths — a match causes the frame to be skipped |

### How to fix
| Attribute    | Default | Description                                                   |
|--------------|---------|---------------------------------------------------------------|
| `how_to_fix` | `UNSET` | Tips on how to resolve the error — displayed in the output    |

### Output format
| Attribute  | Default | Description                                                              |
|------------|---------|--------------------------------------------------------------------------|
| `_oneline` | `False` | When `True`, overrides the active mode and prints the exception on a single line. Useful when a specific call site needs compact output regardless of the configured default mode. |

## Overriding defaults on a subclass
```python
class MyError(SimpleException):
    error_name = "MY_ERROR"
    expected   = "a positive integer"
    how_to_fix = "Provide a value greater than 0."
```

## Notes
- The class itself contains no logic — it is purely declarative.
  All logic lives in the mixins and in `SimpleException.__init__`.
- It serves as the data protocol for `ModeBase.render_message` — the data must
  contain all attributes defined here (they may hold `UNSET`), otherwise
  validation will fail. Internal calls always pass `validate=False`.
- Internal exceptions (`SimpleExceptionInternalError` and its subclasses)
  inherit directly from this class — bypassing `SimpleException` logic
  and avoiding any circular dependency.
"""