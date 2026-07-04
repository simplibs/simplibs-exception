from typing import TYPE_CHECKING
# Inners
from .base_class import ModeBase
from .printers.constants import DOUBLE_LINE, SINGLE_LINE, DOT_PREFIX
from .printers.methods import print_caller_info, print_intro_line, print_value_with_type
# Annotations
if TYPE_CHECKING:
    from ..protocols import ModeBaseProtocol
    from ..protocols import SimpleExceptionDataProtocol


class PrettyMessage(ModeBase):
    """Structured output framed with double lines — the default mode."""

    @staticmethod
    def empty_outcome(
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Output for a call with no data at all.

        ═════════════════════════════════════════════════════════════════
        ⚠️ ERROR: File: ... | Line: ... | Path: ... | Function: ...
        ═════════════════════════════════════════════════════════════════
        """
        return "\n".join((
            DOUBLE_LINE,
            ModeBase.empty_outcome(data),
            DOUBLE_LINE
        ))

    @staticmethod
    def message_outcome(
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Output for message-only calls.

        ═════════════════════════════════════════════════════════════════
        ⚠️ ERROR: Message...
        File: ... | Line: ... | Path: ... | Function: ...
        ═════════════════════════════════════════════════════════════════
        """
        header = f"⚠️ {data.error_name}: {data.message}"
        location = f"\n{print_caller_info(data)}" if data.get_location else ""

        return "\n".join((
            DOUBLE_LINE,
            f"{header}{location}",
            DOUBLE_LINE
        ))

    def full_outcome(
        self: "ModeBaseProtocol",
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Full output with all available fields.

        ═════════════════════════════════════════════════════════════════
        ⚠️ VALIDATION ERROR: data.label
        ═════════════════════════════════════════════════════════════════
        Message:   data.message
        Expected:  data.expected
        Got:       "data.value" (type(data.value))
        Problem:   data.problem
                   ...
        Context:   data.context
        File info: File: ... | Line: ... | Function: ...
        File path: ...
        ─────────────────────────────────────────────────────────────────
        🔧 How to fix:
             • data.how_to_fix
             • ...
        ═════════════════════════════════════════════════════════════════
        Intercepted exception (ValueError):
            Expecting value: line 1 column 1 (char 0)
        """
        # Získání lokace
        location = print_caller_info(data, as_dict=True) if data.get_location else None
        lines = [
            DOUBLE_LINE,
            print_intro_line(data),
            DOUBLE_LINE,

            f"Message:   {data.message}" if data.message else None,
            f"Expected:  {data.expected}" if data.expected else None,
            print_value_with_type(data, intro="Got:       "),
            f"Problem:   {data.problem}" if data.problem else None,
            f"Context:   {data.context}" if data.context else None,
            f"File info: File: {location['file']} | Line: {location['line']} | Function: {location['func']}" if location and location['file'] != "unknown" else None,
            f"File path: {location['path']}" if location and location['path'] != "unknown" else None,

            SINGLE_LINE if data.how_to_fix else None,
            f"🔧 How to fix:{DOT_PREFIX}" + DOT_PREFIX.join(data.how_to_fix) if data.how_to_fix else None,
            DOUBLE_LINE,

            f"Intercepted exception ({data.exception.__name__}):\n"
            f"    {data.intercepted_exception}" if data.intercepted_exception else None,
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
    ⚠️ VALIDATION ERROR: label
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