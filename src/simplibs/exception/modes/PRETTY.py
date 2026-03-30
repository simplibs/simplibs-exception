# Commons
from ..core import SimpleExceptionData
# Inners
from .base_class import ModeBase


# noinspection PyProtectedMember
class PrettyMessage(ModeBase):
    """Structured output framed with double lines — the default mode."""

    # Decorative separators
    double_line = "═" * 65
    single_line = "─" * 65
    prefix = "\n     • "

    def _empty_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """
        Output for a call with no data at all.

        ═════════════════════════════════════════════════════════════════
        ⚠️ ERROR: File: ... | Line: ... | Path: ... | Function: ...
        ═════════════════════════════════════════════════════════════════
        """
        return "\n".join((
            self.double_line,
            super()._empty_outcome(data, caller_info),
            self.double_line
        ))

    def _message_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """
        Output for message-only calls.

        ═════════════════════════════════════════════════════════════════
        ⚠️ ERROR: Message...
        File: ... | Line: ... | Path: ... | Function: ...
        ═════════════════════════════════════════════════════════════════
        """
        return "\n".join((
            self.double_line,
            super()._message_outcome(data, caller_info),
            self.double_line
        ))

    def _full_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """
        Full output with all available fields.

        ═════════════════════════════════════════════════════════════════
        ⚠️ VALIDATION ERROR: value_label
        ═════════════════════════════════════════════════════════════════
        Message:   ...
        Expected:  ...
        Got:       "..." (type)
        Problem:   ...
        Context:   ...
        File info: File: ... | Line: ... | Path: ... | Function: ...
        ─────────────────────────────────────────────────────────────────
        🔧 How to fix:
             • ...
             • ...
        ═════════════════════════════════════════════════════════════════
        Intercepted exception (ValueError):
            Expecting value: line 1 column 1 (char 0)
        """
        lines = [
            self.double_line,
            self._print_intro_line(data),
            self.double_line,

            f"Message:   {data.message}"                         if data.message else None,
            f"Expected:  {data.expected}"                        if data.expected else None,
            self._print_value_with_type(data, intro="Got:       "),
            f"Problem:   {data.problem}"                         if data.problem else None,
            f"Context:   {data.context}"                         if data.context else None,
            f"File info: {self._print_caller_info(caller_info)}" if caller_info else None,

            self.single_line                                     if data.how_to_fix else None,
            f"🔧 How to fix:{self.prefix}" +
            self.prefix.join(data.how_to_fix)                    if data.how_to_fix else None,
            self.double_line,

            f"Intercepted exception ({data.exception.__name__}):\n"
            f"    {data._intercepted_exception}"                 if data._intercepted_exception else None,
        ]
        return "\n".join(line for line in lines if line)


# Singleton mode instance
PRETTY = PrettyMessage()


_DESIGN_NOTES = """
# PRETTY

## Purpose
The default `SimpleException` mode — a structured output framed with double
lines that visually separates the exception from surrounding terminal output.
Designed to reduce cognitive load when reading error output.
If the separator lines are unwanted, `SIMPLE` mode offers identical output
without them.

## Output scenarios

### Empty call
    ═════════════════════════════════════════════════════════════════
    ⚠️ ERROR: File: ... | Line: ... | Path: ... | Function: ...
    ═════════════════════════════════════════════════════════════════

### Message only
    ═════════════════════════════════════════════════════════════════
    ⚠️ ERROR: Message...
    File: ... | Line: ... | Path: ... | Function: ...
    ═════════════════════════════════════════════════════════════════

### Full output
    ═════════════════════════════════════════════════════════════════
    ⚠️ VALIDATION ERROR: value_label
    ═════════════════════════════════════════════════════════════════
    Message:   ...
    Expected:  ...
    Got:       "..." (type)
    Problem:   ...
    Context:   ...
    File info: File: ... | Line: ... | Path: ... | Function: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • ...
         • ...
    ═════════════════════════════════════════════════════════════════
    Intercepted exception (ValueError):
        Expecting value: line 1 column 1 (char 0)

## Fields and their display conditions
All fields are optional — they are displayed only when provided (not UNSET).
The exception is the closing double line, which always appears as the block
terminator. `intercepted_exception` is shown below the closing line as
supplementary information about the original caught exception — deliberately
separated from the main block so it does not add cognitive load in cases
where it is not relevant.

## caller_info
Passed as a parameter from `render_message` in `ModeBase` — resolution
happens centrally there, not inside the mode. If `None` (location disabled
or not found), the `File info` line is not displayed.

## Singleton
The class is used exclusively through the `PRETTY` instance — the mode is
stateless, so there is no reason to create multiple instances.
"""