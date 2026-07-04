from simplibs.sentinels import UNSET
# Outers
from ..SimpleExceptionData import SimpleExceptionData
# Inners
from .mode_base import ModeBase
from .printers.methods import print_caller_info, print_value_with_type


# noinspection PyProtectedMember
class LogMessage(ModeBase):
    """Structured key=value output for log parsers."""

    def empty_outcome(
        self,
        data: SimpleExceptionData
    ) -> str:
        """
        Output for a call with no data at all.
        Format: error=ERROR file='...' line=...
        """
        location = print_caller_info(data, as_dict=True)
        return f"error={data.error_name} file={location['file']!r} line={location['line']}"

    def message_outcome(
        self,
        data: SimpleExceptionData
    ) -> str:
        """
        Output for message-only calls.
        Format: error=ERROR message='...' file='...' line=...
        """
        location = print_caller_info(data, as_dict=True)
        return (
            f"error={data.error_name} "
            f"message={data.message!r} "
            f"file={location['file']!r} line={location['line']}"
        )

    def full_outcome(
        self,
        data: SimpleExceptionData
    ) -> str:
        """
        Full output with all available fields.
        Format: error=ERROR message='...' value='...' file='...' line=...
        """
        location = print_caller_info(data, as_dict=True)

        parts = [
            f"error={data.error_name}",
            f"message={data.message!r}" if data.message else None,
            f"label={data.label!r}" if data.label else None,
            f"value={print_value_with_type(data)!r}" if data.value is not UNSET else None,
            f"expected={data.expected!r}" if data.expected else None,
            f"problem={data.problem!r}" if data.problem else None,
            f"context={data.context!r}" if data.context else None,
            f"file={location['file']!r} line={location['line']}" if data.caller_info else None,

        ]
        return " ".join(part for part in parts if part)


# Singleton mode instance
LOG = LogMessage()


_DESIGN_NOTES = """
# LOG

## Purpose
Output in `key=value` format (logfmt) — designed for machine processing by
log parsers. Each field is explicitly named and space-separated.

## Location Handling
The mode retrieves location data via the `data.caller_info` property. It uses 
the helper method `_print_caller_info(data, as_dict=True)` to obtain a 
dictionary, ensuring that the machine-readable format (`file=... line=...`) 
remains consistent regardless of the global location settings.

## Output scenarios

### Empty call
    error=ERROR file='filename.py' line=42

### Message only
    error=ERROR message='...' file='filename.py' line=42

### Full output
    error=ERROR message='...' label='...' value='...' expected='...' problem='...' context='...' file='filename.py' line=42 how_to_fix='...'

## Field order
1. `error` — the error name
2. `message` — free-form message
3. `label` + `value` — what was being inspected
4. `expected` + `problem` + `context` — error details
5. `file` + `line` — location
6. `how_to_fix` — remediation

## Constraints
- Multi-line fields (like `intercepted_exception`) are excluded to prevent 
  breaking the single-line integrity required by log processors.
- If `data.caller_info` is missing, location fields are omitted from the string.
"""