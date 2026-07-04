from typing import TYPE_CHECKING
# Inners
from .base_class import ModeBase
from .printers.constants import DOUBLE_LINE, SINGLE_LINE, DOT_PREFIX
# from .printers.methods import print_caller_info, print_intro_line, print_value_with_type
# Annotations
if TYPE_CHECKING:
    from ..protocols import ModeBaseProtocol
    from ..protocols import SimpleExceptionDataProtocol

from .printers.methods.full_outcome import (
    print_message,
    print_intro,
    print_expected,
    print_value_with_type,
    print_problem,
    print_context,
    print_how_to_fix,
    print_intercepted_exception,
    print_file_info,
    print_file_path
)
from .printers.methods.message_outcome import print_message_intro

class PrettyMessage(ModeBase):
    """Structured output framed with double lines — the default mode."""

    @staticmethod
    def empty_outcome(
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Output for a call with no data at all.

        ═════════════════════════════════════════════════════════════════
        ⚠️ ERROR NAME: data.label
        File info: File: ... | Line: ... | Function: ...
        File path: ...
        ═════════════════════════════════════════════════════════════════
        """
        lines = [
            DOUBLE_LINE,
            print_intro(data.label, data.error_name),
            print_file_info(data.caller_info),
            print_file_path(data.caller_info),
            DOUBLE_LINE
        ]
        return "\n".join(line for line in lines if line)

    @staticmethod
    def message_outcome(
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Output for message-only calls.

        ═════════════════════════════════════════════════════════════════
        ⚠️ ERROR NAME: data.label
        Message:   data.message
        File info: File: ... | Line: ... | Function: ...
        File path: ...
        ═════════════════════════════════════════════════════════════════
        """
        lines = [
            DOUBLE_LINE,
            print_intro(data.label, data.error_name),
            print_message(data.message),
            print_file_info(data.caller_info),
            print_file_path(data.caller_info),
            DOUBLE_LINE
        ]
        return "\n".join(line for line in lines if line)


    def full_outcome(
        self: "ModeBaseProtocol",
        data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Full output with all available fields.

        ═════════════════════════════════════════════════════════════════
        ⚠️ ERROR NAME: data.label
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
        lines = [
            DOUBLE_LINE,
            print_intro(data.label, data.error_name),
            DOUBLE_LINE,
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value, intro="Got:       "),
            print_problem(data.problem),
            print_context(data.context),
            print_file_info(data.caller_info),
            print_file_path(data.caller_info),
            SINGLE_LINE if data.how_to_fix else None,
            print_how_to_fix(data.how_to_fix),
            DOUBLE_LINE,
            print_intercepted_exception(data.exception, data.intercepted_exception)
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