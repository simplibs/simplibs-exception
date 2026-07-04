from simplibs.sentinels import UNSET
# Outers
from ..core import SimpleExceptionData
# Inners
from .mode_base import ModeBase


# noinspection PyProtectedMember
class OnelineMessage(ModeBase):
    """Compact single-line output for terminal use and quick debugging."""

    def _empty_outcome(self, data: SimpleExceptionData) -> str:
        """
        Output for a call with no data at all.
        Format: ⚠️ ERROR | File: ... | Line: ... | Path: ... | Function: ...
        """
        return f"{self._print_intro_line(data)} | {self._print_caller_info(data)}"

    def _message_outcome(self, data: SimpleExceptionData) -> str:
        """
        Output for message-only calls.
        Format: ⚠️ ERROR: message | File: ... | Line: ... | Path: ... | Function: ...
        """
        return f"{self._print_intro_line(data)}: {data.message} | {self._print_caller_info(data)}"

    def _full_outcome(self, data: SimpleExceptionData) -> str:
        """
        Full output with all available fields.
        Format: ⚠️ ERROR | value_label | Message: ... | Expected: ... | Got: ... | Problem: ... | Context: ... | File: ...
        """
        parts = [
            self._print_intro_line(data),
            f"Message: {data.message}"                    if data.message            else None,
            f"Expected: {data.expected}"                  if data.expected           else None,
            f"Got: {self._print_value_with_type(data)}"   if data.value is not UNSET else None,
            f"Problem: {data.problem}"                    if data.problem            else None,
            f"Context: {data.context}"                    if data.context            else None,
            self._print_caller_info(data)                 if data._get_location      else None,
        ]
        return " | ".join(part for part in parts if part)


# Singleton mode instance
ONELINE = OnelineMessage()


_DESIGN_NOTES = """
# ONELINE

## Purpose
Compact single-line output — all available data on one line, separated by ` | `.
Suited for quick debugging in the terminal where minimizing vertical space 
is critical.

## Location Handling
The mode relies on the `data.caller_info` property. The `_print_caller_info(data)` 
helper provides the formatted string that is appended to the end of the 
output line.

## Output scenarios

### Empty call
    ⚠️ ERROR | File: ... | Line: ... | Path: ... | Function: ...

### Message only
    ⚠️ ERROR: message | File: ... | Line: ... | Path: ... | Function: ...

### Full output
    ⚠️ ERROR: value_label | Message: ... | Expected: ... | Got: ... | Problem: ... | Context: ... | File: ...

## Field order
1. `error_name` + `value_label` — primary identification via `_print_intro_line`
2. `message` — free-form message
3. `expected` — description of the desired state
4. `Got` — the inspected value with its type
5. `problem` — description of the actual error
6. `context` — additional situational information
7. Location — file, line, and function info

## Constraints
- `how_to_fix` is intentionally omitted to keep the output reasonably short.
- If location reporting is disabled, the location segment is skipped entirely.
"""