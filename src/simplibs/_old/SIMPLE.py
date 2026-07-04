# Outers
from ..SimpleExceptionData import SimpleExceptionData
# Inners
from .mode_base import ModeBase
from .printers.constants import DOT_PREFIX
from .printers.methods import print_caller_info, print_intro_line, print_value_with_type


class SimpleMessage(ModeBase):
    """Output without decorative lines — plain text."""

    def full_outcome(
        self,
        data: SimpleExceptionData
    ) -> str:
        """
        Full output with all available fields.

        ⚠️ VALIDATION ERROR: label
        Message:   ...
        Expected:  ...
        Got:       "..." (type)
        Problem:   ...
        Context:   ...
        File info: File: ... | Line: ... | Function: ...
        File path: ...
        🔧 How to fix:
             • ...
             • ...
        Intercepted exception (ValueError):
            Expecting value: line 1 column 1 (char 0)
        """
        loc = print_caller_info(data, as_dict=True) if data._get_location else None
        lines = [
            print_intro_line(data),

            f"Message:   {data.message}" if data.message else None,
            f"Expected:  {data.expected}" if data.expected else None,
            print_value_with_type(data, intro="Got:       "),
            f"Problem:   {data.problem}" if data.problem else None,
            f"Context:   {data.context}" if data.context else None,

            # Rozdělené info o souboru
            f"File info: File: {loc['file']} | Line: {loc['line']} | Function: {loc['func']}"
            if loc and loc['file'] != "unknown" else None,
            f"File path: {loc['path']}" if loc and loc['path'] != "unknown" else None,

            f"🔧 How to fix:{DOT_PREFIX}" +
            DOT_PREFIX.join(data.how_to_fix) if data.how_to_fix else None,
            f"Intercepted exception ({data.exception.__name__}):\n"
            f"    {data._intercepted_exception}" if data._intercepted_exception else None,
        ]
        return "\n".join(line for line in lines if line)


# Singleton mode instance
SIMPLE = SimpleMessage()


_DESIGN_NOTES = """
# SIMPLE

## Purpose
Plain text output without decorative lines — identical content to `PRETTY`
but without the double-line framing. Suited for contexts where separator
lines are visually disruptive or not supported (e.g. some logging systems,
plain text outputs).

## Output scenarios

### Empty call
Inherited from `ModeBase` — intentionally not overridden.
    ⚠️ ERROR: File: ... | Line: ... | Path: ... | Function: ...

### Message only
Inherited from `ModeBase` — intentionally not overridden.
    ⚠️ ERROR: Message...
    File: ... | Line: ... | Path: ... | Function: ...

### Full output
    ⚠️ VALIDATION ERROR: label
    Message:   ...
    Expected:  ...
    Got:       "..." (type)
    Problem:   ...
    Context:   ...
    File info: File: ... | Line: ... | Function: ...
    File path: ...
    🔧 How to fix:
         • ...
         • ...
    Intercepted exception (ValueError):
        Expecting value: line 1 column 1 (char 0)

## Fields and their display conditions
All fields are optional — they are displayed only when provided (not UNSET).
`intercepted_exception` is shown as the last line of the output as supplementary
information about the original caught exception — deliberately last so it does
not add cognitive load in cases where it is not relevant.

## caller_info
Passed as a parameter from `render_message` in `ModeBase` — resolution
happens centrally there, not inside the mode. If `None` (location disabled
or not found), the `File info` line is not displayed.

## Relationship to PRETTY
`SIMPLE` and `PRETTY` produce identical content — the only difference is the
absence of decorative lines. `_empty_outcome` and `_message_outcome` are
intentionally inherited from `ModeBase` without being overridden, as their
default implementations already match the required format.

## Singleton
The class is used exclusively through the `SIMPLE` instance — the mode is
stateless, so there is no reason to create multiple instances.
"""