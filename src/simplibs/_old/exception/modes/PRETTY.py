# Outers
from ..core import SimpleExceptionData
# Inners
from .mode_base import ModeBase


# noinspection PyProtectedMember
class PrettyMessage(ModeBase):
    """Structured output framed with double lines — the default mode."""

    # Decorative separators
    double_line = "═" * 65
    single_line = "─" * 65
    prefix = "\n     • "

    def _empty_outcome(self, data: SimpleExceptionData) -> str:
        """
        Output for a call with no data at all.

        ═════════════════════════════════════════════════════════════════
        ⚠️ ERROR: File: ... | Line: ... | Path: ... | Function: ...
        ═════════════════════════════════════════════════════════════════
        """
        return "\n".join((
            self.double_line,
            super()._empty_outcome(data),
            self.double_line
        ))

    def _message_outcome(self, data: SimpleExceptionData) -> str:
        """
        Output for message-only calls.

        ═════════════════════════════════════════════════════════════════
        ⚠️ ERROR: Message...
        File: ... | Line: ... | Path: ... | Function: ...
        ═════════════════════════════════════════════════════════════════
        """
        header = f"⚠️ {data.error_name}: {data.message}"
        loc = f"\n{self._print_caller_info(data)}" if data._get_location else ""

        return "\n".join((
            self.double_line,
            f"{header}{loc}",
            self.double_line
        ))

    def _full_outcome(self, data: SimpleExceptionData) -> str:
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
        File info: File: ... | Line: ... | Function: ...
        File path: ...
        ─────────────────────────────────────────────────────────────────
        🔧 How to fix:
             • ...
             • ...
        ═════════════════════════════════════════════════════════════════
        Intercepted exception (ValueError):
            Expecting value: line 1 column 1 (char 0)
        """
        # Získání lokace
        loc = self._print_caller_info(data, as_dict=True) if data._get_location else None
        lines = [
            self.double_line,
            self._print_intro_line(data),
            self.double_line,

            f"Message:   {data.message}"                         if data.message else None,
            f"Expected:  {data.expected}"                        if data.expected else None,
            self._print_value_with_type(data, intro="Got:       "),
            f"Problem:   {data.problem}"                         if data.problem else None,
            f"Context:   {data.context}"                         if data.context else None,
            f"File info: File: {loc['file']} | Line: {loc['line']} | Function: {loc['func']}"
                                                                 if loc and loc['file'] != "unknown" else None,
            f"File path: {loc['path']}"                          if loc and loc['path'] != "unknown" else None,

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

## Location Handling
The mode retrieves call site information via the `data.caller_info` property. 
If location reporting is enabled, it is displayed within the `File info` 
section. If no information is available, the line is omitted.

## Output scenarios

### Empty call
A minimal block containing only the error name and location info.
    ═════════════════════════════════════════════════════════════════
    ⚠️ ERROR: File: ... | Line: ... | Path: ... | Function: ...
    ═════════════════════════════════════════════════════════════════

### Message only
A block containing the error name, the free-form message, and location info.
    ═════════════════════════════════════════════════════════════════
    ⚠️ ERROR: Message...
    File: ... | Line: ... | Path: ... | Function: ...
    ═════════════════════════════════════════════════════════════════

### Full output
The most comprehensive format including structured fields (Expected, Got, 
Problem), remediation hints (How to fix), and the origin of the error.
    ═════════════════════════════════════════════════════════════════
    ⚠️ VALIDATION ERROR: value_label
    ═════════════════════════════════════════════════════════════════
    Message:   ...
    Expected:  ...
    Got:       "..." (type)
    Problem:   ...
    Context:   ...
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    ─────────────────────────────────────────────────────────────────
    🔧 How to fix:
         • ...
         • ...
    ═════════════════════════════════════════════════════════════════
    Intercepted exception (ValueError):
        Expecting value: line 1 column 1 (char 0)

## Fields and their display conditions
All fields are optional and are displayed only when they contain data (not UNSET).
`intercepted_exception` is shown below the closing double line as supplementary 
information about the original caught exception.

## Singleton
The class is used exclusively through the `PRETTY` instance. It is stateless 
and designed as a singleton for the entire ecosystem.
"""