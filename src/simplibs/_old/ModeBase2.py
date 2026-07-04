from abc import ABC, abstractmethod
# Outers
from ...protocols import SimpleExceptionDataProtocol
from ..._core_logic.internal_exceptions import SimpleExceptionModeError


class ModeBase(ABC):
    """
    Base class for all SimpleException output modes.

    Enforces the implementation of the core rendering method at runtime.
    """

    @abstractmethod
    def render(self, data: "SimpleExceptionDataProtocol") -> str:
        """
        Main rendering entry point. Must be implemented by individual modes
        to describe their unique layout (Pretty, Simple, Oneline, Log, etc.).
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} mode>"

    def __call__(
        self,
        data: "SimpleExceptionDataProtocol",
        *,
        validate: bool = True
    ) -> str:
        """Shortcut allowing the mode instance to be used directly as a callable."""
        # 1. Volitelná validace datového protokolu
        if validate and not isinstance(data, SimpleExceptionDataProtocol):
            raise SimpleExceptionModeError(
                value=data,
                label="data",
                expected="an object satisfying SimpleExceptionDataProtocol",
                problem="the provided object does not match the expected exception data structure",
                how_to_fix=(
                    "Pass an instance of SimpleExceptionData or any object implementing its protocol.",
                    "For internal calls use validate=False to skip this check.",
                ),
            )

        # 2. Žádné větvení! Pouze delegování práce na konkrétní chameleon-mód.
        return self.render(data)


_DESIGN_NOTES = """
# ModeBase.py

## Purpose
Base class for all `SimpleException` output modes. It defines the interface 
every mode should satisfy, provides default static outcomes, and acts as the 
primary callable entry point for rendering.

## Architecture
The architectural paradigm has shifted from multiple mixins to a lean, decoupled 
"Strategy" pattern. Complex rendering, formatting, and workflow logic have 
been moved into atomic, standalone functions. 

Instead of class inheritance, `ModeBase` and its subclasses collaborate with:
- `render()`  -> Orchestrates the rendering workflow (when to print what).
- `print_intro_line()`   -> Built-in printer helper for the opening line.
- `print_caller_info()`  -> Built-in printer helper for formatting call-site info.

## Interface — What individual modes implement

Three outcome methods that strictly accept only the `data` object:
- `empty_outcome(data) -> str`   [Static default provided]
- `message_outcome(data) -> str` [Static default provided]
- `full_outcome(data) -> str`    [Must be overridden by subclasses]

Note: `caller_info` is entirely managed by the data layer. Subclasses and helper 
functions access it lazily via `data.caller_info`.

## The Callable Interface
The `__call__` method is implemented in `ModeBase` to turn mode instances into 
executable strategies:
```python
PRETTY(data)  # Transparently invokes _render(_render(self, data, validate))

```

## Creating a custom mode

Subclasses no longer need to deal with mixin methods or magic setups. They simply
inherit from `ModeBase` and override `full_outcome`. They can use standalone
printer utilities to build their layout:

```python
class SlackMode(ModeBase):
    def full_outcome(self, data: SimpleExceptionDataProtocol) -> str:
        # Use standalone functions for formatting
        location = print_caller_info(data)
        return f":warning: *{data.error_name}* occurred at {location}"

```

## Notes

* Modes are designed as stateless singleton-like strategy objects.
* It is no longer an ABC; it is a standard base class providing explicit fallbacks.
* Overridden methods should be declared as `@staticmethod` if they do not require
instance state, keeping the ecosystem clean and consistent.
"""