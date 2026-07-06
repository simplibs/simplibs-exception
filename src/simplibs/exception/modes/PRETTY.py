from typing import TYPE_CHECKING
from simplibs.sentinels import UNSET
# Inners
from .base_class import ModeBase
from .printers import (
    DOUBLE_LINE,
    SINGLE_LINE,
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


class PrettyMessage(ModeBase):
    """Structured output framed with double lines — the default presentation mode."""

    def _render(
        self: "ModeBaseProtocol", data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Dynamically adapts and renders the exception into a beautiful framed output.
        Handles empty, message-only, and fully structured data seamlessly.

        The layout engine is fully elastic: it only renders lines for which data has
        been explicitly provided, automatically skipping missing attributes and adjusting
        internal frame dividers. This variability gives you complete control over the final
        output footprint based entirely on the arguments passed to the exception.

        Output Layouts:

            1. Empty Call / Absolute Minimum:
            ═════════════════════════════════════════════════════════════════
            ⚠️ ERROR NAME
            File info: ... | line: ... | function: ...
            File path: ...
            ═════════════════════════════════════════════════════════════════

            2. Message-Only Layout:
            ═════════════════════════════════════════════════════════════════
            ⚠️ ERROR NAME
            Message:   ...
            File info: ... | line: ... | function: ...
            File path: ...
            ═════════════════════════════════════════════════════════════════

            3. Full Structured Layout:
            ═════════════════════════════════════════════════════════════════
            ⚠️ ERROR NAME: label
            ═════════════════════════════════════════════════════════════════
            Message:   ...
            Expected:  ...
            Got:       ... (type)
            Problem:   ...
                       ...
            Context:   ...
                       ...
            File info: ... | line: ... | function: ...
            File path: ...
            ─────────────────────────────────────────────────────────────────
            🔧 How to fix:
                 • ...
                 • ...
            ═════════════════════════════════════════════════════════════════
            Intercepted exception (type):
                ...
        """
        location = data.caller_info

        # Check if we have any granular structured data for the inner body block
        has_details = any(
            [
                data.expected,
                data.value is not UNSET,
                data.problem,
                data.context,
            ]
        )

        lines = [

            # 1. Primary identification header (⚠️ ERROR_NAME: label)
            DOUBLE_LINE,
            print_intro(data.error_name, data.label),

            # 2. Render secondary line ONLY if granular structure details follow
            DOUBLE_LINE if has_details else None,

            # 3. Core body section (Printers return None internally if fields are omitted)
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value),
            print_problem(data.problem),
            print_context(data.context),

            # 4. Shared location metadata components
            print_file_info(location),
            print_file_path(location),

            # 5. Actionable remediation block (How to fix)
            SINGLE_LINE if data.how_to_fix else None,
            print_how_to_fix(data.how_to_fix),
            DOUBLE_LINE,

            # 6. Captured underlying exception block at the absolute bottom
            print_intercepted_exception(data.exception),
        ]

        return "\n".join(line for line in lines if line)


# Singleton mode instance
PRETTY = PrettyMessage()

_DESIGN_NOTES = """
# PRETTY

## Purpose
The default execution mode for `SimpleException`. It renders a rich, highly structured 
terminal output framed within explicit graphical margins. It is optimized for local 
development environments to minimize cognitive load during debugging cycles.

## Adaptive Layout Composition
The renderer is fully elastic and polymorphic. It evaluates the presence of data fields 
dynamically, completely omitting missing properties and adjusting inner layout dividers 
automatically. It guarantees that nothing looks broken or empty, regardless of the usage pattern.

## Output Scenarios

### 1. Empty Call (Absolute Minimum Data)
When no custom message or properties are passed, the mode isolates and prints only 
the primary error identifier header and the physical file location footprint:
```text
═════════════════════════════════════════════════════════════════
⚠️ CORE_ERROR
File info: main.py | line: 12 | function: run_pipeline
File path: /usr/app/src/main.py
═════════════════════════════════════════════════════════════════

```

### 2. Message Only Pattern

If only a free-form description text string is provided, the renderer injects it
directly above the location footprint without rendering the secondary body frame line:

```text
═════════════════════════════════════════════════════════════════
⚠️ DATABASE_ERROR
Message:   Failed to establish a pool connection to the replica.
File info: db.py | line: 84 | function: connect
File path: /usr/app/src/db.py
═════════════════════════════════════════════════════════════════

```

### 3. Full Structured Layout

When fully populated with comparison assertions, multi-line contextual diagnostics,
and mitigation instructions, it builds a full-spectrum report panel:

```text
═════════════════════════════════════════════════════════════════
⚠️ VALIDATION_ERROR: Request Payload Validation Failed
═════════════════════════════════════════════════════════════════
Message:   The submitted account configuration contains illegal data blocks.
Expected:  An active user payload containing a valid enterprise email layout.
Got:       {'email': 'bad_mail', 'tier': 'premium'} (dict)
Problem:   The provided email string does not contain an '@' sign symbol.
           Domain resolution check failed for host 'bad_mail'.
Context:   Client IP: 192.168.1.55
           Request ID: req-9942a-x
File info: validators.py | line: 204 | function: validate_email
File path: /usr/app/src/validators.py
─────────────────────────────────────────────────────────────────
🔧 How to fix:
     • Ensure the input field enforces front-end email format filtering.
     • Check the downstream gateway router payload parser encoding schema.
═════════════════════════════════════════════════════════════════
Intercepted exception (ValueError):
    String validation failed during schema extraction.

```

## Singleton Architecture

The class is completely stateless. It is instantiated exactly once as a module-level
immutable singleton (`PRETTY`). The entire runtime environment references this instance
to prevent thread-safety issues or memory reallocations.
"""
