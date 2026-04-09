from simplibs.sentinels import UNSET
# Outers
from ..base import SimpleExceptionData
# Inners
from .base_class import ModeBase


class OnelineMessage(ModeBase):
    """Compact single-line output for terminal use and quick debugging."""

    def _empty_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """
        Output for a call with no data at all.

        ⚠️ ERROR | File: ... | Line: ... | Path: ... | Function: ...
        """
        return f"⚠️ {data.error_name} | {self._print_caller_info(caller_info)}"

    def _message_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """
        Output for message-only calls.

        ⚠️ ERROR: message | File: ... | Line: ... | Path: ... | Function: ...
        """
        return f"⚠️ {data.error_name}: {data.message} | {self._print_caller_info(caller_info)}"

    def _full_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """
        Full output with all available fields.

        ⚠️ ERROR | value_label | Message: ... | Expected: ... | Got: ... | Problem: ... | Context: ... | File: ...
        """
        parts = [
            f"⚠️ {data.error_name}",
            data.value_label                              if data.value_label        else None,
            f"Message: {data.message}"                    if data.message            else None,
            f"Expected: {data.expected}"                  if data.expected           else None,
            f"Got: {self._print_value_with_type(data)}"   if data.value is not UNSET else None,
            f"Problem: {data.problem}"                    if data.problem            else None,
            f"Context: {data.context}"                    if data.context            else None,
            self._print_caller_info(caller_info)          if caller_info             else None,
        ]
        return " | ".join(part for part in parts if part)


# Singleton mode instance
ONELINE = OnelineMessage()


_DESIGN_NOTES = """
# ONELINE

## Purpose
Compact single-line output — all available data on one line, separated by ` | `.
Suited for quick debugging in the terminal or wherever minimising the number
of output lines is important.

Activated via the `oneline=True` parameter when raising the exception:
    raise SimpleException(problem="Something went wrong", oneline=True)

## What is intentionally omitted
`how_to_fix` is not displayed — remediation tips are typically longer texts
that would make the single-line output impractically long and reduce readability.
For output with remediation hints, use `PRETTY` or `SIMPLE`.

## Output scenarios

### Empty call
    ⚠️ ERROR | File: ... | Line: ... | Path: ... | Function: ...

### Message only
    ⚠️ ERROR: message | File: ... | Line: ... | Path: ... | Function: ...

### Full output
    ⚠️ ERROR | value_label | Message: ... | Expected: ... | Got: ... | Problem: ... | Context: ... | File: ...

## Field order
1. `error_name` — always present
2. `value_label` — label for the inspected value
3. `message` — free-form message
4. `expected` — what was expected
5. `Got` — the inspected value with its type
6. `problem` — description of the error
7. `context` — additional situational information
8. caller info — location in the code

## caller_info
Passed as a parameter from `render_message` in `ModeBase`. If `None`
(location disabled or not found), the caller info is not displayed.

## Singleton
The class is used exclusively through the `ONELINE` instance — the mode is
stateless, so there is no reason to create multiple instances.
"""