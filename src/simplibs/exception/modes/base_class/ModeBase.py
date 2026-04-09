from abc import ABC, abstractmethod
from simplibs.sentinels import UNSET
# Outers
from ...utils import extract_caller_info
from ...base import SimpleExceptionData
# Inners
from ._mixins import PrintCallerInfoMixin, PrintIntroLineMixin, PrintValueWithTypeMixin


class ModeBase(
    PrintCallerInfoMixin,       # def _print_caller_info(self, caller_info: dict | None, as_dict: bool = False) -> str | dict
    PrintIntroLineMixin,        # def _print_intro_line(self, data: SimpleExceptionData) -> str
    PrintValueWithTypeMixin,    # def _print_value_with_type(self, data: SimpleExceptionData, *, intro: str = "") -> str | None
    ABC
):
    """Abstract base class for all SimpleException output modes."""

    # -------------------------------------------------------------------------
    # Abstract methods — _full_outcome is required, the others have defaults
    # -------------------------------------------------------------------------

    def _empty_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """Output for a call with no data at all — displays only the location."""
        return f"⚠️ {data.error_name}: {self._print_caller_info(caller_info)}"

    def _message_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """Output for message-only calls — displays the message and location."""
        return (
            f"⚠️ {data.error_name}: {data.message}"
            f"\n{self._print_caller_info(caller_info)}"
        )

    @abstractmethod
    def _full_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """Full output with all available fields — must be implemented by subclasses."""
        ...

    # -------------------------------------------------------------------------
    # Public entry point
    # -------------------------------------------------------------------------
    # noinspection PyProtectedMember
    def render_message(self, data: SimpleExceptionData, *, validate: bool = True) -> str:
        """
        Selects the appropriate output based on the data content and returns the assembled string.

        Args:
            data:     Exception data conforming to SimpleExceptionData.
            validate: If True, verifies that the data matches the expected protocol.

        Returns:
            The assembled exception output string.
        """
        # 1. Optional data validation — skipped on internal calls from _build_message()
        if validate:
            from ._validations import validate_has_simple_exception_data
            validate_has_simple_exception_data(data)

        # 2. Detect whether content fields are present for a full output
        has_base_content = not (
            data.value is UNSET
            and data.expected is UNSET
            and data.problem is UNSET
            and data.context is UNSET
            and data.how_to_fix is UNSET
        )

        # 3. Resolve caller_info — done once here at a predictable stack depth
        caller_info = (
            extract_caller_info(
                skip_frames=data._get_location + 1,
                excluded_patterns=data._skip_locations
            )
            if data._get_location
            else None
        )

        # 4. Select the appropriate output based on data content
        if not has_base_content:
            if data.message is UNSET:
                return self._empty_outcome(data, caller_info)
            return self._message_outcome(data, caller_info)
        return self._full_outcome(data, caller_info)

    def __call__(self, data: SimpleExceptionData, *, validate: bool = True) -> str:
        """Shortcut for render_message() — allows the instance to be used as a callable."""
        return self.render_message(data, validate=validate)

    # -------------------------------------------------------------------------
    # Dunder methods
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} mode>"


_DESIGN_NOTES = """
# ModeBase

## Purpose
Abstract base class for all `SimpleException` output modes — defines the
interface every mode must implement, shared helper methods, and the logic
for selecting the correct output based on data content.

## Data interface
All methods accept `SimpleExceptionData` as input — they therefore require
the presence of all attributes defined in that class. Modes work with data
only, not with exception behaviour.

## render_message — processing flow

### Step 1 — data validation
If `validate=True` (default), the provided object is verified to be an
instance of `SimpleExceptionData`. For internal calls where the data is
already guaranteed to be correct (e.g. from `SimpleException._build_message()`)
`validate=False` is passed and this step is skipped.

The validation function is loaded lazily:
    from ._validations import validate_has_simple_exception_data

The lazy import is necessary — `ModeBase` lives in `modes` and a standard
top-level import of `_validations` would pull in `SimpleExceptionModeError` →
`SimpleExceptionInternalError` → `modes` again. The lazy import breaks this
cycle and loads the validation only when it is actually needed.

### Step 2 — scenario detection
`has_base_content` checks whether at least one content field is present:
`value`, `expected`, `problem`, `context`, `how_to_fix`. If none of these
are provided, the call is either empty or message-only.
`message` is deliberately excluded from this check — it serves as an
alternative to the structured fields, not as part of them.

### Step 3 — caller_info resolution
`extract_caller_info` is called once here in `render_message` and the result
is passed as an explicit `caller_info` argument to all output methods.

The resolution deliberately happens here and not inside `_print_caller_info` —
the reason is stack depth. If `extract_caller_info` were called inside
`_print_caller_info`, the stack would be several levels deeper
(`render_message` → `_full_outcome` → `_print_caller_info` → `extract_caller_info`)
and the value of `skip_frames` would need to vary depending on which output
method called `_print_caller_info`. Centralising the resolution in
`render_message` guarantees that `skip_frames` is always correct and predictable.

If `data._get_location` is falsy, `caller_info` is `None` — location
reporting is intentionally disabled and no resolution takes place.

### Step 4 — output selection

| Scenario      | Condition                                              | Method           |
|---------------|--------------------------------------------------------|------------------|
| Empty call    | no content fields and no message provided              | _empty_outcome   |
| Message only  | message provided, no content fields present            | _message_outcome |
| Full output   | at least one content field is present                  | _full_outcome    |

## Output method signatures
All three output methods accept the same parameters:
    def _*_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str

`caller_info` is either a dictionary with keys `file`, `full_path`, `line`,
`function`, or `None` if location reporting is disabled or no frame was found.

## Required implementation
Subclasses must implement `_full_outcome` — the full output with all fields.
`_empty_outcome` and `_message_outcome` have default implementations
that can be overridden.

## Helper methods (from mixins)
- `_print_caller_info(caller_info, as_dict=False)` — formats the provided
  caller_info as a string or dictionary
- `_print_intro_line(data)` — builds the opening line with error_name and value_label
- `_print_value_with_type(data, intro=...)` — builds a value representation with its type

## How to create a custom mode
    from .base_class.ModeBase import ModeBase

    class MyMode(ModeBase):

        def _full_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
            return f"[{data.error_name}] {data.message}"

    MY_MODE = MyMode()

A mode should be a singleton — one instance per ecosystem.
This is not a structural requirement but a convention: modes are stateless,
so there is no reason to create multiple instances.

## Notes
- `__call__` delegates to `render_message()` — mode instances can be used
  as callables: `PRETTY(data)`.
- The class inherits from `ABC` — it cannot be instantiated directly,
  only its subclasses can.
"""