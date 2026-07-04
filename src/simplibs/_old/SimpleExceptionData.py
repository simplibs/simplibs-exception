from typing import Any
from dataclasses import dataclass
from simplibs.sentinels import UNSET, UnsetType
# Inners
from ._core_logic.data_methods import create_caller_info


@dataclass
class SimpleExceptionData:
    """Data class defining the structure and default values of SimpleException."""

    # --- Core exception info ---
    error_name: str = "ERROR"
    exception: type[Exception] | UnsetType = UNSET
    intercepted_exception: str | UnsetType = UNSET

    # --- Info about the inspected value ---
    value: object = UNSET
    label: str | UnsetType = UNSET

    # --- Exception description ---
    expected: str | UnsetType = UNSET
    problem: str | UnsetType = UNSET
    context: str | UnsetType = UNSET
    message: str | UnsetType = UNSET

    # --- How to fix ---
    how_to_fix: tuple[str, ...] | None = None

    # --- Location info ---
    get_location: int | bool = True
    skip_locations: tuple[str, ...] = ()
    _cached_caller_info: dict[str, Any] | UnsetType = UNSET

    # --- Single-line output ---
    oneline: bool = False

    # -------------------------------------------------------------------------
    # Property
    # -------------------------------------------------------------------------

    @property
    def caller_info(self):
        """
        Lazily-computed and cached call site information.

        Returns:
            Dictionary with keys: file, full_path, line, function
            Or None if location reporting is disabled or frame not found.

        Caching:
            Computes only once — result is cached in _cached_caller_info.
            Subsequent accesses return the cached value immediately.
        """
        self._cached_caller_info = create_caller_info(
            self._cached_caller_info,
            self.get_location,
            self.skip_locations
        )
        return self._cached_caller_info


_DESIGN_NOTES = """
# SimpleExceptionData.py

# SimpleExceptionData — Flat Data Layer

## Purpose
A pure data class defining the structure, default values, and interface of `SimpleException`.
It serves as the unified, single source of truth for exception state across the entire 
library, ensuring that data is completely separated from formatting and rendering workflows.

## Location Awareness & Decoupling
Instead of using deep mixin hierarchies, `SimpleExceptionData` achieves location awareness 
by encapsulating a lazy `@property def caller_info`. 
1. **Decoupled Introspection**: The heavy lifting of stack introspection is delegated 
   to the standalone function `create_caller_info()`.
2. **Universal Access**: Both public exceptions and internal library errors can 
   utilize this identical data structure to report call-site origins.
3. **Simplified Renderers**: Output modes (strategies) receive this data object 
   and can trust that all necessary fields—including location data—are readily accessible.

## Underscore Convention
- **Without underscore**: Diagnostic data fields and public options intended for 
  the user, formatting modes, and serializators (e.g., `to_dict()`).
- **With underscore**: Purely internal mechanics managed automatically by the library, 
  such as configuration flags for tracing or the internal cache.

## Attribute Reference

### Core Info
| Attribute               | Default   | Description                                          |
|-------------------------|-----------|------------------------------------------------------|
| `error_name`            | `"ERROR"` | Error name displayed in the output                   |
| `exception`             | `UNSET`   | Exception class for dynamic dynamic MRO ancestors   |
| `intercepted_exception` | `UNSET`   | A text description/traceback of a caught exception   |

### Inspected Value
| Attribute     | Default | Description                                               |
|---------------|---------|-----------------------------------------------------------|
| `value`       | `UNSET` | The actual object/value that caused the failure           |
| `label`       | `UNSET` | Human-readable label for the value (e.g., `"parameter"`) |

### Exception Description
| Attribute  | Default | Description                                                      |
|------------|---------|------------------------------------------------------------------|
| `expected` | `UNSET` | Description of the desired/valid state                           |
| `problem`  | `UNSET` | Description of what exactly went wrong                           |
| `context`  | `UNSET` | Additional situational or environment information                |
| `message`  | `UNSET` | Free-form alternative message bypassing structured fields        |

### How to Fix
| Attribute    | Default | Description                                                   |
|--------------|---------|---------------------------------------------------------------|
| `how_to_fix` | `UNSET` | Remediation tips and bullet points displayed in the output    |

### Location Mechanics (Internal)
| Attribute             | Default | Description                                                                 |
|-----------------------|---------|-----------------------------------------------------------------------------|
| `_get_location`       | `True`  | Enable/disable reporting or set the explicit stack depth offset             |
| `_skip_locations`     | `()`    | Path patterns or filenames to filter out during stack introspection         |
| `_cached_caller_info` | `UNSET` | Internal cache to store the computed caller dict                           |

### Output Format Configuration
| Attribute | Default | Description                                                              |
|-----------|---------|--------------------------------------------------------------------------|
| `oneline` | `False` | When `True`, signals that a compact single-line output layout is desired|

## Notes
- Objects of this class satisfy the `SimpleExceptionDataProtocol` required by render modes.
- **Lazy Performance**: Tracing the call stack is a relatively heavy operation. The 
  `_cached_caller_info` cache is only populated upon the very first access to `data.caller_info`. 
  If an output mode or a user never requests the location, no introspection occurs.
"""