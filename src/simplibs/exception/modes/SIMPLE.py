from typing import TYPE_CHECKING
# Inners
from .base_class import ModeBase
from .printers import (
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
# Annotations
if TYPE_CHECKING:
    from ..protocols import ModeBaseProtocol
    from ..protocols import SimpleExceptionDataProtocol


class SimpleMessage(ModeBase):
    """Output without decorative lines — plain text layout."""

    def _render(
        self: "ModeBaseProtocol", data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Dynamically adapts and renders the exception into a clean plain text layout.
        Handles empty, message-only, and fully structured data seamlessly.

        The layout engine is fully elastic: it only renders lines for which data has
        been explicitly provided, automatically skipping missing attributes. This variability
        gives you complete control over the final output footprint based entirely on the
        arguments passed to the exception, maintaining a clean layout without decorative frame lines.

        Output Layouts:

            1. Empty Call / Absolute Minimum:
            ⚠️ ERROR NAME
            File info: ... | line: ... | function: ...
            File path: ...

            2. Message-Only Layout:
            ⚠️ ERROR NAME
            Message:   ...
            File info: ... | line: ... | function: ...
            File path: ...

            3. Full Structured Layout:
            ⚠️ ERROR NAME: label
            Message:   ...
            Expected:  ...
            Got:       ... (type)
            Problem:   ...
                       ...
            Context:   ...
                       ...
            File info: ... | line: ... | function: ...
            File path: ...
            🔧 How to fix:
                 • ...
                 • ...
            Intercepted exception (type):
                ...
        """
        location = data.caller_info

        lines = [
            # 1. Primary identification header (⚠️ ERROR_NAME: label)
            print_intro(data.error_name, data.label),

            # 2. Core exception details (Printers return None if values are omitted)
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value),
            print_problem(data.problem),
            print_context(data.context),

            # 3. Shared location metadata components
            print_file_info(location),
            print_file_path(location),

            # 4. Actionable remediation block (How to fix)
            print_how_to_fix(data.how_to_fix),

            # 5. Captured underlying exception block at the absolute bottom
            print_intercepted_exception(data.exception),
        ]

        # Join only existing segments—empty rows caused by missing data dissolve instantly
        return "\n".join(line for line in lines if line)


# Singleton mode instance
SIMPLE = SimpleMessage()


_DESIGN_NOTES = """
# SIMPLE

## Purpose
A plain text presentation mode that delivers identical structural content to `PRETTY`, 
but entirely strips away all decorative frame lines (`DOUBLE_LINE`, `SINGLE_LINE`). 
It is ideal for minimal terminals, standard output pipes, or logging channels 
where box-drawing characters are visually disruptive or cause encoding issues.

## Adaptive Layout Composition
Just like the default mode, `SIMPLE` is fully elastic. It prints only fields that 
contain live runtime data. If properties are left unconfigured, they are omitted without 
leaving awkward gaps or breaking the vertical alignment.

## Output Scenarios

### 1. Empty Call (Absolute Minimum Data)
When no custom parameters or messages are provided, it presents only the error header 
and the immediate source file resolution matrix:
```text
⚠️ CORE_ERROR
File info: main.py | line: 12 | function: run_pipeline
File path: /usr/app/src/main.py

```

### 2. Message Only Pattern

If a single free-form string is supplied, it drops cleanly into place right beneath
the header, maintaining a compact flat profile:

```text
⚠️ DATABASE_ERROR
Message:   Failed to establish a pool connection to the replica.
File info: db.py | line: 84 | function: connect
File path: /usr/app/src/db.py

```

### 3. Full Structured Layout

When packed with all diagnostic properties, it forms a perfectly aligned plain text block:

```text
⚠️ VALIDATION_ERROR: Request Payload Validation Failed
Message:   The submitted account configuration contains illegal data blocks.
Expected:  An active user payload containing a valid enterprise email layout.
Got:       {'email': 'bad_mail', 'tier': 'premium'} (dict)
Problem:   The provided email string does not contain an '@' sign symbol.
           Domain resolution check failed for host 'bad_mail'.
Context:   Client IP: 192.168.1.55
           Request ID: req-9942a-x
File info: validators.py | line: 204 | function: validate_email
File path: /usr/app/src/validators.py
🔧 How to fix:
     • Ensure the input field enforces front-end email format filtering.
     • Check the downstream gateway router payload parser encoding schema.
Intercepted exception (ValueError):
    String validation failed during schema extraction.

```

## Singleton Architecture

The class is completely stateless. It is instantiated exactly once as a module-level
immutable singleton (`SIMPLE`). The entire ecosystem reuse this shared pointer
to guarantee maximum execution performance and zero memory thrashing.
"""


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
               ...
    Context:   ...
               ...
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
Passed as a parameter from `render` in `ModeBase` — resolution
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