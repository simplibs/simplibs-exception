from typing import TYPE_CHECKING
# Inners
from .modes import PRETTY
from ._core_logic.settings_meta import SettingsMeta
from ._core_logic.internal_exceptions import SimpleExceptionSettingsError
# Annotations
if TYPE_CHECKING:
    from .protocols import ModeBaseProtocol


class SimpleExceptionSettings(metaclass=SettingsMeta):
    """Central configuration registry — the single source of truth for the entire exception ecosystem."""

    # --- System Blacklist (Read-Only) ---
    # Visible for maximum architectural transparency, but sealed at the metaclass layer.
    _SYSTEM_BLACKLIST: tuple[str, ...] = ("<", "simplibs/exception")

    # --- Live Configuration Attributes ---
    GET_LOCATION: int | bool = 1
    LOCATION_BLACKLIST: tuple[str, ...] = _SYSTEM_BLACKLIST
    MESSAGE_MODE: "ModeBaseProtocol" = PRETTY
    VALUE_TRUNCATION_LENGTH: int = 70

    # --- Internal Cache ---
    _dynamic_cls_cache: dict[
        tuple[type[BaseException], type[BaseException]], type[BaseException]
    ] = {}

    # --- Prevent Instantiation ---
    def __init__(self) -> None:
        raise SimpleExceptionSettingsError(
            label="SimpleExceptionSettings",
            problem="This configuration registry class is not intended to be instantiated.",
            how_to_fix=(
                "Access or modify configuration attributes directly on the class: SimpleExceptionSettings.GET_LOCATION",
                "To restore factory defaults programmatically, call: SimpleExceptionSettings.reset()",
            ),
        )

    # --- Reset to Default Factory Values ---
    @classmethod
    def reset(cls) -> None:
        """Resets all operational settings and internal caches back to their factory default values."""
        cls.GET_LOCATION = 1
        cls.LOCATION_BLACKLIST = ()
        cls.VALUE_TRUNCATION_LENGTH = 70
        cls.MESSAGE_MODE = PRETTY
        cls._dynamic_cls_cache = {}


_DESIGN_NOTES = """
# SimpleExceptionSettings

## Purpose
Acts as the global, central runtime configuration registry and the single source of truth for the 
behavioral characteristics of all exceptions within the ecosystem. Attributes are stateful and can 
be dynamically modified or reset at runtime. The class serves strictly as a monolithic static namespace 
and is intentionally locked against instantiation.

## Configuration Attributes Reference

### _SYSTEM_BLACKLIST (System-Protected & Read-Only)
A protected system-level matrix containing core patterns that are unconditionally excluded during stack trace traversal:
- `"<"`: Bypasses Python internal dynamic virtual frames (`<string>`, `<frozen importlib>`, `<lambda>`).
- `"simplibs/exception"`: Automatically suppresses the library's own internal execution noise.

This attribute is fully exposed within the settings registry to maintain absolute design transparency 
for developers inspecting the ecosystem. However, it is explicitly omitted from factory reset routines 
and strictly blacklisted against manual modifications at the metaclass layer to guarantee system stability.

### GET_LOCATION
Controls the activation state and traversal depth behavior of the runtime call-site filesystem scanner.

| Value     | Behavioral Outcome                                                                     |
|-----------|-----------------------------------------------------------------------------------------|
| `False`   | Completely mutes location reporting; `caller_info` property evaluates to `None`.        |
| `True`    | Captures the immediate external user code frame that initialized the error (Depth: 1).  |
| `int`     | Traverses the call stack down to a custom integer depth boundary.                       |

*Note: Individual exception parameter overrides take absolute precedence over this global registry fallback value.*

### LOCATION_BLACKLIST
A customizable tuple of directory fragments, package strings, or filenames matched against execution traceback frames. 
If an active stack path contains any string defined here, the execution trace engine discards that frame.
```python
SimpleExceptionSettings.LOCATION_BLACKLIST = ("my_project/decorators",)
# Dynamically drops all execution frames executing inside the user-defined path wrapper.

```

*Note: This user blacklist works in tandem with `_SYSTEM_BLACKLIST`. The runtime scanner automatically
merges both lists before scanning.*

### MESSAGE_MODE

An instance of a presentation strategy satisfying `ModeBaseProtocol`. It governs the default layout
compilation matrix when generating terminal exception displays.

```python
SimpleExceptionSettings.MESSAGE_MODE = PRETTY   # Graphical double-line boxed framing panel (Default)
SimpleExceptionSettings.MESSAGE_MODE = SIMPLE   # Structured clean layout without border rules
SimpleExceptionSettings.MESSAGE_MODE = ONELINE  # Ultra-compact, horizontal pipe-delimited stream
SimpleExceptionSettings.MESSAGE_MODE = LOG      # Production logfmt key=value serialized line format

```

⚠️ **Architectural Guardrail**: Custom layout strategies must never query `SimpleExceptionSettings` attributes.
The relationship must remain strictly one-way: settings consume modes, modes remain completely agnostic of settings.
Violating this constraint introduces circular package initialization loops.

### VALUE_TRUNCATION_LENGTH

An integer specifying the maximum acceptable string size boundary for objects inspected inside error structures.

| Bound | Behavioral Outcome |
| --- | --- |
| `int` | Maximum length of `repr(value)` allowed into the compiler stream before clipping (Default: 70) |

When an evaluation object exceeds this limit, the engine truncates the string text and appends a safe token counter
identifying omitted characters (e.g., `[truncated, 452 chars]`). This shields developer terminal interfaces from
being flooded by massive dict structures or database raw dumps.

### _dynamic_cls_cache

An internal private dictionary map backing the dynamic multi-inheritance interception layer. It is not intended
for client modification. It maps combination keys `(ExceptionClass, ForeignExceptionClass)` to synthetic virtual
types spawned on-the-fly during runtime execution cycles, saving significant compiler CPU overhead.

## Factory Resets

To wipe live state adjustments and rollback all parameters to baseline production defaults, execute:

```python
SimpleExceptionSettings.reset()

```

## Structural Validation Metaclass

The registry uses `SettingsMeta` as its metaclass. `SettingsMeta` intercepts all `__setattr__` operations
at runtime, running data type assertions and value constraints against incoming overrides to catch
invalid values immediately before they can corrupt downstream presentation components.
"""