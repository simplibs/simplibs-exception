# Commons
from ..modes.base_class import ModeBase
from ..modes import PRETTY
# Inners
from ._meta import SimpleExceptionSettingsMeta, SimpleExceptionSettingsError


class SimpleExceptionSettings(metaclass=SimpleExceptionSettingsMeta):
    """Central configuration — the single source of truth for the entire ecosystem."""

    # --- Default values ---
    DEFAULT_GET_LOCATION: int | bool = 1
    DEFAULT_LOCATION_BLACKLIST: tuple[str, ...] = ()
    DEFAULT_MESSAGE_MODE: ModeBase = PRETTY

    # --- Cache ---
    _dynamic_cls_cache: dict[tuple, type[BaseException]] = {}

    # --- Prevent instantiation ---
    def __init__(self):
        raise SimpleExceptionSettingsError(
            value_label="SimpleExceptionSettings",
            problem="this class is not intended to be instantiated",
            how_to_fix=(
                "Access attributes directly on the class: SimpleExceptionSettings.DEFAULT_GET_LOCATION",
                "To reset all values use: SimpleExceptionSettings.reset()",
            ),
        )

    # --- Reset to default values ---
    @classmethod
    def reset(cls):
        """Resets all settings to their factory defaults."""
        cls.DEFAULT_GET_LOCATION = 1
        cls.DEFAULT_LOCATION_BLACKLIST = ()
        cls.DEFAULT_MESSAGE_MODE = PRETTY
        cls._dynamic_cls_cache = {}


_DESIGN_NOTES = """
# SimpleExceptionSettings

## Purpose
The central configuration of the library — the single source of truth for the
default behaviour of all exceptions in the ecosystem. Values can be overridden
or reset at runtime. The class is not intended to be instantiated — all
attributes are accessed directly on the class.

## Attributes

### DEFAULT_GET_LOCATION
Controls whether and from where call site location information is retrieved.

| Value   | Behaviour                                                  |
|---------|------------------------------------------------------------|
| `False` | Location is not reported                                   |
| `True`  | Reports the location of the direct caller (default)        |
| `int`   | Reports the location at the given stack depth              |

If the user overrides this value when raising an exception, their value takes
precedence. The recommended values for global configuration are `True` / `False`
— a higher integer only makes sense in specific cases where additional stack
layers need to be skipped.

### DEFAULT_LOCATION_BLACKLIST
A tuple of strings matched against the full file path — if a string is found,
that frame is skipped during location resolution.
```python
DEFAULT_LOCATION_BLACKLIST = ("simple_exception",)
# skips all frames whose path contains "simple_exception"
```

Each item must be a `str`. The string `"<"` for skipping Python's dynamic
frames (`<string>`, `<frozen importlib>`, etc.) is added internally by
`extract_caller_info` — it never needs to be defined here.

### DEFAULT_MESSAGE_MODE
An instance of a class derived from `ModeBase` — determines the default output
format for exceptions. One of the built-in modes or a custom mode can be used:
```python
DEFAULT_MESSAGE_MODE = PRETTY   # default — structured output with separator lines
DEFAULT_MESSAGE_MODE = SIMPLE   # plain text without decorations
DEFAULT_MESSAGE_MODE = ONELINE  # single-line output
DEFAULT_MESSAGE_MODE = LOG      # key=value format for log parsers
```

A custom mode must inherit from `ModeBase` and implement `_full_outcome()`.

⚠️ Important — a mode must not reference `SimpleExceptionSettings` or any of
its attributes. The entire system is designed so that modes are completely
independent of settings — settings consumes modes, not the other way around.
This rule must be followed for custom modes as well, otherwise a circular
dependency will arise.

### _dynamic_cls_cache
An internal dictionary for caching dynamically created classes — not intended
for manual assignment, only for reset via `reset()`.

It is populated exclusively by `DunderNewMixin.__new__` on the first encounter
of a `(exception class, exception type)` combination — each unique combination
is created once and then repeatedly retrieved from the cache. Manual writes
to this attribute are not supported.

## Reset to factory defaults
```python
SimpleExceptionSettings.reset()
```
Returns all attributes to the default values defined in this class.

## Validation
The class uses the `SimpleExceptionSettingsMeta` metaclass, which intercepts
every attempt to set an attribute via `__setattr__` and verifies the validity
of the provided value. Details of the validation logic are described in the
`SimpleExceptionSettingsMeta` documentation.
"""