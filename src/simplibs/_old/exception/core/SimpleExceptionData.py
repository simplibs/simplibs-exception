from typing import Any
from dataclasses import dataclass
from simplibs.sentinels import UNSET, UnsetType
# Inners
from ._data_mixin import CallerInfoMixin


@dataclass
class SimpleExceptionData(CallerInfoMixin):
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
    _cached_caller_info: dict[str, Any] | UnsetType = UNSET

    # --- Single-line output ---
    _oneline: bool = False


_DESIGN_NOTES = """
# SimpleExceptionData

## Purpose
A data class defining the structure, default values, and interface of `SimpleException`.
It serves as a shared foundation for the entire library. By inheriting from 
`CallerInfoMixin`, it becomes "location-aware", allowing any exception (including 
internal ones) to lazily compute its origin.

## Inheritance and Logic
While primarily a data container, inheriting from `CallerInfoMixin` provides the 
`caller_info` property. This ensures that:
1. **Logic is decoupled**: Introspection logic stays in the mixin.
2. **Universal access**: Both `SimpleException` and `SimpleExceptionInternalError` 
   can report their location via the same interface.
3. **Renderers are simplified**: Output modes can rely solely on the data 
   object to provide all necessary information, including call site details.

## Underscore convention
- **Without underscore** — input parameters for users/subclasses.
- **With underscore** — values managed automatically (e.g., `_cached_caller_info`).

## Attribute reference

### Core info
| Attribute               | Default   | Description                                          |
|-------------------------|-----------|------------------------------------------------------|
| `error_name`            | `"ERROR"` | Error name displayed in the output                   |
| `exception`             | `UNSET`   | Exception class for the MRO                          |
| `_intercepted_exception`| `UNSET`   | Automatically set description of a caught exception  |

### Inspected value
| Attribute     | Default | Description                                               |
|---------------|---------|-----------------------------------------------------------|
| `value`       | `UNSET` | The value that caused the error                           |
| `value_label` | `UNSET` | Label for the value (e.g., `"parameter age"`)             |

### Exception description
| Attribute  | Default | Description                                                      |
|------------|---------|------------------------------------------------------------------|
| `expected` | `UNSET` | Description of the desired state                                 |
| `problem`  | `UNSET` | Description of what is wrong                                     |
| `context`  | `UNSET` | Additional situational info                                      |
| `message`  | `UNSET` | Free-form alternative message                                    |

### Location
| Attribute            | Default | Description                                                                 |
|----------------------|---------|-----------------------------------------------------------------------------|
| `_get_location`      | `True`  | Enable/disable reporting or set stack depth                                 |
| `_skip_locations`    | `()`    | Path patterns to skip during stack introspection                            |
| `_cached_caller_info`| `UNSET` | Internal cache for the `caller_info` property                               |

### How to fix
| Attribute    | Default | Description                                                   |
|--------------|---------|---------------------------------------------------------------|
| `how_to_fix` | `UNSET` | Remediation tips displayed in the output                      |

### Output format
| Attribute  | Default | Description                                                              |
|------------|---------|--------------------------------------------------------------------------|
| `_oneline` | `False` | When `True`, forces a compact single-line output format.                 |

## Notes
- It serves as the data protocol for `ModeBase.render_message`.
- **Lazy Caching:** The `_cached_caller_info` is populated only when `data.caller_info` 
  is first accessed. This saves performance if the location is never needed.
"""