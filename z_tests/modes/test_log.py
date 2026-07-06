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


class LogMessage(ModeBase):
    """Machine-readable key-value output adhering to the logfmt specification."""

    def _render(
        self: "ModeBaseProtocol", data: "SimpleExceptionDataProtocol"
    ) -> str:
        """
        Dynamically adapts and flattens all available exception fields into
        a single space-separated logfmt string.

        ## Full output preview:
        error=ERROR message='...' label='...' value='...' expected='...' problem='...' context='...' file='filename.py' line=42 how_to_fix='...'

        ## Field order
        1. `error_name` + `label` — primary identification via `_print_intro_line`
        2. `message` — free-form message
        3. `expected` — description of the desired state
        4. `Got` — the inspected value with its type
        5. `problem` — description of the actual error
        6. `context` — additional situational information
        7. Location — file, line, and function info
        """
        location = data.caller_info

        lines = [
            # 1. Primary identification header (error=... or error=... label=...)
            print_intro(data.error_name, data.label, _log_mode=True),

            # 2. Structured core attributes (Printers handle safe !r quoting natively)
            print_message(data.message, _log_mode=True),
            print_expected(data.expected, _log_mode=True),
            print_value_with_type(data.value, _log_mode=True),
            print_problem(data.problem, _log_mode=True),
            print_context(data.context, _log_mode=True),

            # 3. Location tracing metadata
            print_file_info(location, _log_mode=True),
            print_file_path(location, _log_mode=True),
        ]

        # Join only active tokens into a perfectly flat, single-line log stream token row
        return " ".join(line for line in lines if line)


# Singleton mode instance
LOG = LogMessage()


_DESIGN_NOTES = """
# LOG

## Purpose
A machine-readable execution mode that formats all active exception properties 
into standard `key=value` serialization (logfmt). It is explicitly engineered 
for production container injection streams, centralized log aggregators (Elasticsearch, 
Datadog, AWS CloudWatch), and index-heavy routing engines.

## Token Serialization Integrity
By delegating execution to low-level printers with `_log_mode=True`, the formatter 
guarantees that unsafe string components (containing spaces, quotes, or control characters) 
are automatically sanitized via Python's native `repr()` wrapper (`!r`). This ensures that 
downstream token parsers read each property as a single bounded value without line splitting.

## Output Scenarios

### 1. Empty Call (Absolute Minimum Data)
When called with zero optional parameters, it maps down to structural tracing data:
```text
error='CORE_ERROR' file='main.py' line=12 function='run_pipeline' path='/usr/app/src/main.py'

```

### 2. Message Only Pattern

```text
error='DATABASE_ERROR' message='Failed to establish a pool connection to the replica.' file='db.py' line=84 function='connect' path='/usr/app/src/db.py'

```

### 3. Full Structured Layout

When fully populated, all complex types are flattened and space-separated chronologically:

```text
error='VALIDATION_ERROR' label='Request Payload Validation Failed' message='The submitted account configuration contains illegal data blocks.' expected='An active user payload containing a valid enterprise email layout.' value="{'email': 'bad_mail', 'tier': 'premium'}" type='dict' problem='The provided email string does not contain an \x27@\x27 sign symbol. Domain resolution check failed for host \x27bad_mail\x27.' context='Client IP: 192.168.1.55 Request ID: req-9942a-x' file='validators.py' line=204 function='validate_email' path='/usr/app/src/validators.py'

```

## Structural Constraints & Pruning Choices

* **Strictest Single-Line Policy**: Newline characters are forbidden.
* `how_to_fix` checklists are **omitted entirely**. Remediation paths are descriptive human instructions, which would only bloat log indexes.
* `intercepted_exception` trace blocks are **pruned down to their class names** inside `print_intercepted_exception` to prevent dirty multi-line stack trace drops into a clean stdout pool.
* If `data.caller_info` is unallocated, location keys (`file`, `line`, `function`, `path`) completely dissolve from the generated row.

## Singleton Architecture

The class is completely stateless. It is instantiated exactly once as a module-level
immutable singleton (`LOG`). All components utilize this single reference to prevent allocation overhead.
"""

