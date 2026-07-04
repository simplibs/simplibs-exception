from typing import TYPE_CHECKING, Any
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .SimpleExceptionData import SimpleExceptionData
from ._core_logic.lifecycle.init_utils import (
    normalize_string,
    normalize_strings,
    normalize_exception,
    normalize_bool,
    process_get_location,
    process_skip_locations,
    assemble_message
)
from ._core_logic.lifecycle.init_subclass import check_children_attributes
from ._core_logic.lifecycle.new_method import add_exception_type
from ._core_logic.tracing import with_location_offset as _with_location_offset
# Annotations
if TYPE_CHECKING:
    from .protocols import SimpleExceptionProtocol


class SimpleException(SimpleExceptionData, Exception):
    """Structured runtime exception engine optimized for the Simple ecosystem."""

    # -------------------------------------------------------------------------
    # __init__ — attribute assignment and message assembly
    # -------------------------------------------------------------------------

    def __init__(
        self,
        message: str | None = None,
        *,
        value: Any = UNSET,
        label: str | None = None,
        expected: str | None = None,
        problem: str | tuple[str, ...] | list[str] | None = None,
        context: str | tuple[str, ...] | list[str] | None = None,
        how_to_fix: str | tuple[str, ...] | list[str] | None = None,
        error_name: str | None = None,
        exception: Exception | type[Exception] | None = None,
        get_location: bool | int | None = None,
        skip_locations: tuple[str, ...] | str | None = None,
        oneline: bool = False,
    ) -> None:
        # --- Core metadata ---
        self.error_name = normalize_string(self, error_name, "error_name")
        self.exception = normalize_exception(self, exception)

        # --- Inspected value ---
        self.value = value
        self.label = normalize_string(self, label, "label")

        # --- Exception description ---
        self.expected = normalize_string(self, expected, "expected")
        self.message = normalize_string(self, message, "message")
        self.problem = normalize_strings(self, problem, "problem")
        self.context = normalize_strings(self, context, "context")

        # --- Actionable remediation ---
        self.how_to_fix = normalize_strings(self, how_to_fix, "how_to_fix")

        # --- Location metadata options ---
        self.get_location = process_get_location(get_location)
        self.skip_locations = process_skip_locations(skip_locations)

        # --- Layout overrides ---
        self.oneline = normalize_bool(self, oneline, "oneline")

        # --- Compile the visual terminal text footprint ---
        self.rendered_message = assemble_message(self, oneline)

        # --- Initialize Exception base class, bypassing dataclass __init__ in MRO ---
        Exception.__init__(self, self.rendered_message)

    # -------------------------------------------------------------------------
    # Dunder methods
    # -------------------------------------------------------------------------

    def __new__(
        cls,
        *args: Any,
        exception: type[Exception] | UnsetType = UNSET,
        **kwargs: Any
    ) -> "SimpleExceptionProtocol":
        """
        Dynamically injects a foreign exception type into the class ancestors (MRO) if provided.
        """
        return add_exception_type(cls, exception)

    def __init_subclass__(
        cls,
        **kwargs: Any
    ) -> None:
        """
        Validates the contract of concrete subclasses during definition to catch syntax typos early.
        """
        super().__init_subclass__(**kwargs)
        check_children_attributes(SimpleExceptionData, cls)

    def __str__(self) -> str:
        """
        Returns the fully compiled visual layout string block representation of the exception.
        """
        return self.rendered_message

    def __repr__(self) -> str:
        """
        Returns an unambiguous engineering string representation containing the class identity.
        """
        return f"<{self.__class__.__name__}(error_name={self.error_name!r})>"

    # -------------------------------------------------------------------------
    # Transformators
    # -------------------------------------------------------------------------

    def with_location_offset(
        self: "SimpleExceptionProtocol", offset: int = 1
    ) -> "SimpleExceptionProtocol":
        """
        Spawns a modified clone of this exception with an adjusted file-tracking stack lookup depth.
        """
        return _with_location_offset(self, offset)


_DESIGN_NOTES = """
# SimpleException

## Purpose
The primary, executable operational component of the error framework. It merges the pure 
data state storage of `SimpleExceptionData` with the native python control-flow capabilities 
of `Exception`. It orchestrates dynamic type interception, subclass safety audits, 
and text output generation.

## Separation of Concerns (Role Architecture)
- **Data & Serialization (`SimpleExceptionData`)**: Acts as the passive data model. It owns the parameters, 
  lazy property caching, and public analytics state exporters (`to_dict()`, `to_json()`).
- **Runtime & Execution (`SimpleException`)**: Acts as the active execution manager. It normalizes inputs, 
  assembles the final rendering block layout, controls inheritance, and provides runtime mutation tools.

## Initialization Lifecycle & MRO Management
1. **Dynamic MRO Mutation (`__new__`)**: Before allocation occurs, `__new__` checks for intercepted exception signatures. 
   If one exists, it mutates the class graph dynamically so that standard `except CapturedError:` hooks trigger seamlessly.
2. **Subclass Typos Guard (`__init_subclass__`)**: Runs at compile/import time to prevent developers from defining illegal 
   properties on custom sub-exceptions, catching naming errors before production execution.
3. **MRO Intercept Bypass**: Dataclasses automatically generate an `__init__` that resets fields. `SimpleException.__init__` 
   explicitly overrides this, normalizes properties via `init_utils`, and bypasses dataclass initialization by 
   directly invoking `Exception.__init__(self, self.rendered_message)`.

## Environment Magic Hooks
- **`__str__`**: Controls the text stream interface. It maps directly to `self.rendered_message`, causing terminals, 
  test frameworks, and traceback loggers to print the cleanly structured formatting panel natively.
- **`__repr__`**: Delivers a concise developer signature. It references `self.__class__.__name__` ensuring that 
  even dynamically generated virtual class paths reveal their runtime categories accurately during inspection.

## Transformative Re-raising
The `with_location_offset()` method allows wrappers or catch-and-raise middleware patterns to offset the 
file lookup boundary. It clones the current error structure with increased inspection depth, ensuring that the 
rendered output points directly to the real application layer code rather than internal routing blocks.
"""