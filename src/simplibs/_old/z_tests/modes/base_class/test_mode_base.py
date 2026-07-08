from abc import ABC, abstractmethod
# Outers
from ...core_logic.internal_exceptions import SimpleExceptionModeError
from ...protocols import SimpleExceptionDataProtocol


class ModeBase(ABC):
    """
    Base class for all SimpleException output modes.

    Implements the Template Method pattern to enforce a unified public API
    with built-in validation, while delegating the layout logic to subclasses.
    """

    @abstractmethod
    def _render(self, data: "SimpleExceptionDataProtocol") -> str:
        """
        Internal abstract method. Must be implemented by concrete subclasses
        (e.g., PrettyMode, OnelineMode) to define their unique layout.
        """
        pass

    def render(
        self,
        data: "SimpleExceptionDataProtocol",
        *,
        validate: bool = True
    ) -> str:
        """
        Public entry point for rendering exception data into a formatted string.

        Handles structural validation and dispatches the data to the concrete
        layout implementation.
        """
        # 1. Optional data structure validation
        if validate:
            if not hasattr(data, "message") or not hasattr(data, "error_name"):
                raise SimpleExceptionModeError(
                    value=data,
                    label="data",
                    expected="an object satisfying SimpleExceptionDataProtocol",
                    problem="the provided object does not match the expected exception data structure",
                    how_to_fix=(
                        "Pass an instance of SimpleExceptionData or any object implementing its protocol.",
                        "For trusted internal calls, use validate=False to skip this check.",
                    ),
                )

        # 2. Delegate the actual layout rendering to the concrete subclass
        return self._render(data)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} mode>"


_DESIGN_NOTES = """
# ModeBase

## Purpose
Serves as the abstract foundation for all exception rendering styles (e.g., Pretty, 
Oneline, Log). It establishes a rigid contractual interface for the layout engine 
and guarantees robust data safety.

## Architectural Pattern: Template Method
This class strictly adheres to the **Template Method** design pattern:
- **`render()` (Public API)**: The single, immutable entryway. It contains shared, 
  reusable logic — specifically data validation. It is *not* meant to be overridden.
- **`_render()` (Protected SPI - Service Provider Interface)**: A purely abstract method 
  implemented by concrete subclasses to define their specific string layouts.

## Prevention of Accidental Overrides
By marking `_render` as the only `@abstractmethod`, Python's native ABC mechanism 
protects the public `render` method from being accidentally wiped out by custom 
user modes. If a developer incorrectly overrides `render` instead of `_render`, 
the ABC runtime will block instantiation with a clear `TypeError` pointing out 
that the abstract `_render` method is still missing.

## Validation Strategy & Duck-Typing Philosophy
The validation pipeline is explicitly split based on the execution context to achieve 
an optimal balance between raw runtime speed and public API bulletproofing:

### 1. Internal Fast-Path (`validate=False`)
When exceptions are compiled natively by the library framework (via `assemble_message`), the internal 
engine fully trusts the data structures and passes `validate=False`. This eliminates expensive 
attribute checking entirely, ensuring that throwing an exception has near-zero performance overhead.

### 2. Public Safety Net (`validate=True`)
Mode singletons (like `PRETTY`, `ONELINE`) are exposed publicly. If a developer calls a mode 
manually outside the native exception lifecycle, the entry point triggers an explicit check for the 
absolute structural minimums: `error_name` and `message`. 
- **Why not check the entire Protocol?** Instead of using restrictive `isinstance` checks against the full 
  `SimpleExceptionDataProtocol` (which is slow and overly rigid), the architecture utilizes **duck-typing** via `hasattr`. If a mode is fed an object with at least an error identifier and a core message text, 
  the underlying printer ecosystem is robust enough to gracefully skip all other missing variables.

### Real-World Decoupled Scenarios
This benevolent validation design transforms the formatting suite into a powerful, standalone 
mini-framework, unlocking two critical architectural use-cases:
- **Isolated Testing (Mocking)**: When writing unit tests for custom layout modes, developers do not 
  need to instantiate heavy runtime `SimpleException` states. They can pass a lightweight mock object or 
  a simple dataclass containing only `error_name` and `message`, keeping the test suite agile and isolated.
- **Centralized Log Pipelines**: In complex application frameworks (e.g., custom HTTP middleware), developers 
  can catch raw exception data payloads and defer formatting until the absolute edge of the application 
  lifecycle. This allows them to dynamically feed the data object into different modes (e.g., shifting to 
  `LOG` in production but rendering `PRETTY` in local development dashboards) completely dynamically.

## Usage
Custom modes subclass `ModeBase` and implement `_render`:
```python
class MyCustomMode(ModeBase):
    def _render(self, data):
        return f"[{data.error_name}] -> {data.message}"
"""