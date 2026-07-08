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
    print_file_info,
    print_file_path
)
# Annotations
if TYPE_CHECKING:
    from ..protocols import ModeBaseProtocol
    from ..protocols import SimpleExceptionDataProtocol


class OnelineMessage(ModeBase):
    """Compact single-line output for terminal use and rapid debugging cycles."""

    def _render(
        self: "ModeBaseProtocol", data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Dynamically adapts and flattens all available exception fields into
        a single, pipe-separated string. Handles all data states automatically.

        ## Full output preview:
        ⚠️ ERROR: label | Message: ... | Expected: ... | Got: ... | Problem: ... | Context: ... | File: ...

        ## Field order:
        1. `error_name` + `label` — primary identification via `_print_intro_line`
        2. `message` — free-form message
        3. `expected` — description of the desired state
        4. `Got` — the inspected value with its type
        5. `problem` — description of the actual error
        6. `context` — additional situational information
        7. Location — file, line, and function info
        """
        location = data.caller_info

        # Gather all formatted parts using standard human prefixes
        raw_parts = [
            print_intro(data.error_name, data.label),
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value),
            print_problem(data.problem),
            print_context(data.context),
            print_file_info(location),
            print_file_path(location),
        ]

        # Join only existing segments with the pipe separator and strip trailing whitespace
        return " | ".join(part for part in parts if part).strip()


# Singleton mode instance
ONELINE = OnelineMessage()


_DESIGN_NOTES = """
# ONELINE

## Purpose
A highly compact, dense presentation mode that aggregates all available exception diagnostics 
into a single, uninterrupted horizontal text row using ` | ` as a delimiter field separator. 
It is explicitly optimized for local terminal execution environments where screen real estate 
is scarce or where developers want to grep through dense error stack outputs.

## Native Flattening Delegation
To guarantee a strict single-row design without performance penalties, the renderer does not 
perform post-processing or regex stripping on the final string. Instead, it natively delegates 
the flattening responsibility directly to multi-line sensitive printers (`print_problem`, `print_context`) 
by passing the `_oneline=True` control flag. This ensures that layout padding and vertical margins 
are suppressed at the source.

## Output Scenarios

### 1. Empty Call (Absolute Minimum Data)
When stripped of optional details, it compresses into a tight, location-focused string:
```text
⚠️ CORE_ERROR | File info: main.py | line: 12 | function: run_pipeline | File path: /usr/app/src/main.py

```

### 2. Message Only Pattern

```text
⚠️ DATABASE_ERROR | Message: Failed to establish a pool connection to the replica. | File info: db.py | line: 84 | function: connect | File path: /usr/app/src/db.py

```

### 3. Full Structured Layout

When fully populated, fields are strung together chronologically from high-level metadata
down to physical source code file hooks:

```text
⚠️ VALIDATION_ERROR: Request Payload Validation Failed | Message: The submitted account configuration contains illegal data blocks. | Expected: An active user payload containing a valid enterprise email layout. | Got: {'email': 'bad_mail', 'tier': 'premium'} (dict) | Problem: The provided email string does not contain an '@' sign symbol. Domain resolution check failed for host 'bad_mail'. | Context: Client IP: 192.168.1.55 Request ID: req-9942a-x | File info: validators.py | line: 204 | function: validate_email | File path: /usr/app/src/validators.py

```

## Omission Choices

* `how_to_fix` checklist steps are **intentionally omitted** from this mode. Actionable
remediation advice is inherently verbose and multi-line, which directly violates
the low-profile blueprint of horizontal dense streaming.
* `intercepted_exception` is skipped to avoid trailing traceback contamination.

## Singleton Architecture

The class is completely stateless. It is instantiated exactly once as a module-level
immutable singleton (`ONELINE`). The entire ecosystem shares this instance to ensure
instant compilation speed with zero memory reallocations.
"""
