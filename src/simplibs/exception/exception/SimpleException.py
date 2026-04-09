from simplibs.sentinels import UNSET, UnsetType
# Outers
from ..base import SimpleExceptionData
from ..settings import SimpleExceptionSettings as S
# Inners
from ._mixins.dunders import DunderInitSubclassMixin, DunderNewMixin
from ._mixins.serializers import ToDictMixin, ToDebugDictMixin, ToJsonMixin
from ._mixins.normalizers import (
    NormalizeParamMixin,
    ProcessExceptionParamMixin,
    ProcessHowToFixParamMixin,
    ProcessSkipLocationsParamMixin,
    ProcessGetLocationParamMixin
)


class SimpleException(
    # Base class
    SimpleExceptionData,            # Base class with class-level attributes
    # Dunders
    DunderInitSubclassMixin,        # def __init_subclass__(cls, **kwargs) -> None
    DunderNewMixin,                 # def __new__(cls, *args, exception: type[Exception] | UnsetType, **kwargs) -> None
    # Normalizers
    NormalizeParamMixin,            # def _normalize_param(self, value: Any, attr: str, typ: type) -> Any
    ProcessExceptionParamMixin,     # def _process_exception_param(self, value: type[Exception]) -> tuple[type[Exception] | UnsetType, str | UnsetType]
    ProcessHowToFixParamMixin,      # def _process_how_to_fix_param(self, value: tuple[str, ...] | str | UnsetType) -> tuple[str, ...] | UnsetType
    ProcessSkipLocationsParamMixin, # def _process_skip_locations_param(self, value: tuple[str, ...] | list[str] | str | UnsetType) -> tuple[str, ...]
    ProcessGetLocationParamMixin,   # def _process_get_location_param(self, value: int | bool | UnsetType) -> int | bool
    # Serializers
    ToDictMixin,                    # def to_dict(self) -> dict
    ToDebugDictMixin,               # def to_debug_dict(self) -> dict
    ToJsonMixin,                    # def to_json(self) -> str
    # Base exceptions
    Exception                       # Base exception enabling the raise mechanism
):
    """Structured exception for the Simple ecosystem."""


    # -------------------------------------------------------------------------
    # __init__ — attribute assignment and message assembly
    # -------------------------------------------------------------------------

    def __init__(
        self,
        message: str | UnsetType = UNSET,
        *,
        value: object = UNSET,
        value_label: str | UnsetType = UNSET,
        expected: str | UnsetType = UNSET,
        problem: str | UnsetType = UNSET,
        context: str | UnsetType = UNSET,
        how_to_fix: tuple[str, ...] | str | UnsetType = UNSET,
        error_name: str | UnsetType = UNSET,
        exception: Exception | type[Exception] | UnsetType = UNSET,
        get_location: bool | int | UnsetType = UNSET,
        skip_locations: tuple[str, ...] | str | UnsetType = UNSET,
        oneline: bool = False,
    ):

        # --- Core info ---
        self.error_name = self._normalize_param(error_name, "error_name", str)
        self.exception, self._intercepted_exception = self._process_exception_param(exception)

        # --- Inspected value ---
        self.value = value
        self.value_label = self._normalize_param(value_label, "value_label", str)

        # --- Exception description ---
        self.expected = self._normalize_param(expected, "expected", str)
        self.problem = self._normalize_param(problem, "problem", str)
        self.context = self._normalize_param(context, "context", str)
        self.message = self._normalize_param(message, "message", str)

        # --- How to fix ---
        self.how_to_fix = self._process_how_to_fix_param(how_to_fix)

        # --- Location ---
        self._get_location = self._process_get_location_param(get_location)
        self._skip_locations = self._process_skip_locations_param(skip_locations)

        # --- Single-line output ---
        self._oneline = self._normalize_param(oneline, "oneline", bool)

        # --- Assemble the message ---
        self._rendered_message = self._render_message()

        # --- Initialise Exception — bypasses the dataclass __init__ in the MRO ---
        Exception.__init__(self, self._rendered_message)


    # -------------------------------------------------------------------------
    # Message assembly — delegates to the output mode
    # -------------------------------------------------------------------------

    def _render_message(self) -> str:
        """Passes the data to the active mode and returns the assembled string."""
        if self._oneline:
            from ..modes import ONELINE
            return ONELINE(self, validate=False)
        return S.DEFAULT_MESSAGE_MODE(self, validate=False)


    # -------------------------------------------------------------------------
    # Dunder methods
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(error_name={self.error_name!r}, value={self.value!r})>"

    def __str__(self) -> str:
        return self._rendered_message


_DESIGN_NOTES = """
# SimpleException

## Purpose
The core class of the ecosystem — a structured exception that combines a data
layer, validation, normalisation, and output modes into a single unit. Designed
so that the exception itself communicates with the developer — describing the
cause, the circumstances, and the path to a fix.

## Class composition
`SimpleException` is assembled from mixins, each with a single responsibility:

### Data layer
- `SimpleExceptionData` — class-level attributes and default values, the source
  of truth for all parameters. Subclasses can override them.

### Dunders
- `DunderInitSubclassMixin` — validates subclasses at definition time,
  catching typos and incorrect types immediately on import.
- `DunderNewMixin` — dynamically adds `exception` to the instance ancestors,
  enabling `isinstance(e, ValueError)` without static inheritance.

### Normalizers
- `NormalizeParamMixin` — normalises simple parameters based on a type check.
  If the value does not match the expected type, the class-level default is
  returned. Never raises an exception.
- `ProcessExceptionParamMixin` — processes the `exception` parameter,
  accepting both an exception class and an exception instance. Handles the
  fallback to the class-level default internally when no value is provided —
  consistent with the other normalisation methods.
- `ProcessHowToFixParamMixin` — normalises the `how_to_fix` parameter,
  accepting `str`, `tuple[str, ...]`, or `list[str]` and normalising to
  `tuple[str, ...]`. Falls back to the class-level default.
- `ProcessGetLocationParamMixin` — processes the `get_location` parameter,
  returning the provided value or `S.DEFAULT_GET_LOCATION` from settings.
  Unlike other normalisations, the fallback comes from settings rather than
  the class-level default — `get_location` is a global library setting.
- `ProcessSkipLocationsParamMixin` — processes the `skip_locations` parameter,
  normalises the input to `tuple[str, ...]` and merges it with
  `S.DEFAULT_LOCATION_BLACKLIST`. The merge happens inside the method —
  the user's blacklist and the global blacklist always apply together.

### Serializers
- `ToDictMixin` — public attributes as a dictionary, UNSET values omitted.
- `ToDebugDictMixin` — public and private computed attributes as a dictionary.
- `ToJsonMixin` — public attributes as a JSON string.

## Private vs public attributes
Attributes are divided by their semantics:

**Public** — exception data, included in `to_dict()`:
    error_name, exception, value, value_label,
    expected, problem, context, message, how_to_fix

**Private** — behavioural configuration and computed values, only in `to_debug_dict()`:
    _get_location, _skip_locations, _oneline,
    _intercepted_exception, _rendered_message

## Output modes
The message is assembled in `_render_message()`, which delegates to a mode:
- `_oneline=True` — uses the `ONELINE` mode (lazy import)
- otherwise — uses `S.DEFAULT_MESSAGE_MODE` (default: `PRETTY`)

The lazy import of `ONELINE` in `_render_message` is intentional — it prevents
a circular dependency between the `exception` and `modes` modules.

## Processing flow in `__init__`
    1. Normalise core info (error_name, exception)
    2. Normalise the inspected value (value, value_label)
    3. Normalise the exception description (expected, problem, context, message)
    4. Process how_to_fix
    5. Process location (_get_location, _skip_locations)
    6. Set the output format (_oneline)
    7. Assemble the message via _render_message()
    8. Pass the message to Exception.__init__()

## How to create a custom exception
    class MyValidationError(SimpleException):
        error_name = "VALIDATION ERROR"
        expected   = "a positive integer"
        how_to_fix = (
            "Provide a value greater than 0.",
            "Use the int type.",
        )

    raise MyValidationError(value=age, value_label="parameter age")

Class-level attributes overridden on the subclass take precedence over
parameters — they can always be overridden again at the call site.

## Using the exception parameter
    # As a class:
    raise SimpleException(exception=ValueError, problem="negative value")

    # As an instance from an except block:
    try:
        ...
    except ValueError as e:
        raise SimpleException(exception=e, problem="negative value")

## Notes
- `_render_message` stores the result in `self._rendered_message` — a private
  attribute that `__str__` returns directly. `self.message` remains a clean
  input parameter accessible via `to_dict()`.
- All normalisation methods are designed to never raise an exception —
  in the worst case they return the class-level default or the settings value.
"""