from abc import ABC, abstractmethod
# Outers
from ...core import SimpleExceptionData
# Inners
from ._mixins import (
    RenderMessageMixin,
    PrintCallerInfoMixin,
    PrintIntroLineMixin,
    PrintValueWithTypeMixin,
)


class ModeBase(
    RenderMessageMixin,         # render_message(self, data: SimpleExceptionData, *, validate = True) -> str
    PrintCallerInfoMixin,       # _print_caller_info(self, data: SimpleExceptionData, *, as_dict: bool = False) -> str | dict[str, Any]
    PrintIntroLineMixin,        # _print_intro_line(self, data: SimpleExceptionData) -> str
    PrintValueWithTypeMixin,    # _print_value_with_type(self, data: SimpleExceptionData, *, intro: str = "", max_length: int | None = None) -> str | None
    ABC
):
    """Abstract base class for all SimpleException output modes.

    Defines the interface every mode must implement and provides shared
    helper methods. Subclasses must implement _full_outcome().
    """

    # -------------------------------------------------------------------------
    # Interface — default implementations and required abstract method
    # -------------------------------------------------------------------------

    def _empty_outcome(self, data: SimpleExceptionData) -> str:
        """Output for a call with no data at all — displays only the location."""
        return f"{self._print_intro_line(data)} {self._print_caller_info(data)}"

    def _message_outcome(self, data: SimpleExceptionData) -> str:
        """Output for message-only calls — displays the message and location."""
        return (
            f"⚠️ {data.error_name}: {data.message}"
            f"\n{self._print_caller_info(data)}"
        )

    @abstractmethod
    def _full_outcome(self, data: SimpleExceptionData) -> str:
        """Full output with all available fields — must be implemented by subclasses."""
        ...

    # -------------------------------------------------------------------------
    # Dunder methods
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} mode>"

    def __call__(self, data: SimpleExceptionData, *, validate: bool = True) -> str:
        """Shortcut for render_message() — allows the instance to be used as a callable."""
        return self.render_message(data, validate=validate)


_DESIGN_NOTES = """
# ModeBase — Updated Architecture

## Purpose
Abstract base class for all `SimpleException` output modes. Defines the
interface every mode must implement, provides shared helper methods, and
acts as the primary entry point for rendering.

## Architecture
The class is composed of multiple mixins. By centralizing the `caller_info` 
logic into the data layer, the interface of `ModeBase` has been significantly 
simplified:

    RenderMessageMixin       -> Workflow logic (when to print what)
    PrintCallerInfoMixin     -> Formatting call site info (from data)
    PrintIntroLineMixin      -> Building the opening line
    PrintValueWithTypeMixin  -> Formatting values with types

## Interface — What subclasses implement

Three output methods that now strictly accept only the `data` object:
    def _empty_outcome(data) -> str
    def _message_outcome(data) -> str
    def _full_outcome(data) -> str  ← ABSTRACT

Note: `caller_info` is no longer passed as an argument. Subclasses and 
helpers access it via `data.caller_info` (lazy property).

## Helper methods (from mixins)
Available for use in output methods:
    - _print_caller_info(data, as_dict=False)
        Formats caller info from data as a string or dictionary
    - _print_intro_line(data)
        Builds the opening line (⚠️ ERROR_NAME: label)
    - _print_value_with_type(data, intro="...", max_length=None)
        Formats value with type and handles truncation logic.

## The Callable Interface
The `__call__` method is implemented here to make mode instances callable:
    PRETTY(data)  # Equivalent to PRETTY.render_message(data)

## Creating a custom mode

    class SlackMode(ModeBase):
        def _full_outcome(self, data: SimpleExceptionData) -> str:
            return f":warning: *{data.error_name}* at {self._print_caller_info(data)}"

## Notes
- Modes are singletons.
- The class cannot be instantiated directly (ABC).
- All helper methods now follow a unified signature: they accept `data`.
"""