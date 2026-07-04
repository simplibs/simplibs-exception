from typing import Any
from dataclasses import dataclass
from simplibs.sentinels import UNSET, UnsetType
# Inners
from ._core_logic.data_methods import extract_caller_info


@dataclass
class SimpleExceptionData:
    """Data class defining the structure and default values of SimpleException."""

    # --- Core exception info ---
    error_name: str = "ERROR"
    exception: type[Exception] | None = None
    intercepted_exception: str | None = None

    # --- Info about the inspected value ---
    # Zde sentinel MUSÍ zůstat, protože hodnota může být doslova cokoliv (včetně None)
    value: Any = UNSET

    # --- Exception description ---
    label: str | None = None
    expected: str | None = None
    problem: str | None = None
    context: str | None = None
    message: str | None = None

    # --- How to fix ---
    how_to_fix: tuple[str, ...] | None = None

    # --- Location info ---
    get_location: int | bool = True
    skip_locations: tuple[str, ...] = ()
    _cached_caller_info: dict[str, Any] | None | UnsetType = UNSET

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
        # 1. If location reporting is disabled, store None and exit
        if not self.get_location:
            return None

        # 2. Compute information using extract_caller_info
        # _get_location acts as expected_frames (1 = first user frame)
        if self._cached_caller_info is UNSET:
            self._cached_caller_info = extract_caller_info(
                expected_frames=int(self.get_location),
                excluded_patterns=self.skip_locations
            )

        # 3. Return the cached value or None
        return self._cached_caller_info


_DESIGN_NOTES = """
# SimpleExceptionData.py

## Purpose
A pure data class defining the structure, default values, and interface of `SimpleException`.
It serves as the unified, single source of truth for exception state across the entire 
library, ensuring that data is completely separated from formatting and rendering workflows.

## Location Awareness & Decoupling
Instead of using deep mixin hierarchies, `SimpleExceptionData` achieves location awareness 
by encapsulating a smart, lazy `@property def caller_info`. 
1. **Direct Property Logic**: The property itself handles the orchestration of the 
   internal cache. If the cache is empty, it delegates the heavy stack introspection 
   directly to the standalone function `extract_caller_info()`.
2. **Universal Access**: Both public exceptions and internal library errors can 
   utilize this identical data structure to report call-site origins.
3. **Simplified Renderers**: Output modes (strategies) receive this data object 
   and can trust that all necessary fields—including location data—are readily accessible.

## Underscore Convention
- **Without underscore**: Diagnostic data fields and public options intended for 
  the user, formatting modes, and serializers (e.g., `to_dict()`).
- **With underscore**: Purely internal mechanics managed automatically by the library, 
  specifically the internal cache for saving computed performance resources.

## Attribute Reference

### Core Info
| Attribute               | Default   | Description                                          |
|-------------------------|-----------|------------------------------------------------------|
| `error_name`            | `"ERROR"` | Error name displayed in the output                   |
| `exception`             | `None`    | Exception class for dynamic dynamic MRO ancestors   |
| `intercepted_exception` | `None`    | A text description/traceback of a caught exception   |

### Inspected Value
| Attribute     | Default | Description                                               |
|---------------|---------|-----------------------------------------------------------|
| `value`       | `UNSET` | The actual object/value that caused the failure (Any type)|

### Exception Description
| Attribute  | Default | Description                                                      |
|------------|---------|------------------------------------------------------------------|
| `label`    | `None`  | Human-readable label for the value (e.g., `"parameter"`)         |
| `expected` | `None`  | Description of the desired/valid state                           |
| `problem`  | `None`  | Description of what exactly went wrong                           |
| `context`  | `None`  | Additional situational or environment information                |
| `message`  | `None`  | Free-form alternative message bypassing structured fields        |

### How to Fix
| Attribute    | Default | Description                                                   |
|--------------|---------|---------------------------------------------------------------|
| `how_to_fix` | `None`  | Remediation tips and bullet points displayed in the output    |

### Location Mechanics
| Attribute             | Default | Description                                                                 |
|-----------------------|---------|-----------------------------------------------------------------------------|
| `get_location`        | `True`  | Enable/disable reporting or set the explicit stack depth offset             |
| `skip_locations`      | `()`    | Path patterns or filenames to filter out during stack introspection         |
| `_cached_caller_info` | `UNSET` | Internal cache to store the computed caller dict or `None` if not found     |

### Output Format Configuration
| Attribute | Default | Description                                                              |
|-----------|---------|--------------------------------------------------------------------------|
| `oneline` | `False` | When `True`, signals that a compact single-line output layout is desired|

## Notes
- Objects of this class satisfy the `SimpleExceptionDataProtocol` required by render modes.
- **Lazy Performance & Non-Intrusive None**: Tracing the call stack is a relatively heavy 
  operation. The `_cached_caller_info` cache remains `UNSET` until the very first access 
  to `data.caller_info`. If the introspection returns `None` (on failure), this `None` is 
  safely cached as a valid result, preventing subsequent redundant stack traversals.
"""