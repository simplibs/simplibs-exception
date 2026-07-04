from simplibs.sentinels import UNSET
# Outers
from ..core import SimpleExceptionData
# Inners
from .mode_base import ModeBase


# noinspection PyProtectedMember
class LogMessage(ModeBase):
    """Structured key=value output for log parsers."""

    def _empty_outcome(self, data: SimpleExceptionData) -> str:
        """
        Output for a call with no data at all.
        Format: error=ERROR file='...' line=...
        """
        loc = self._print_caller_info(data, as_dict=True)
        return f"error={data.error_name} file={loc['file']!r} line={loc['line']}"

    def _message_outcome(self, data: SimpleExceptionData) -> str:
        """
        Output for message-only calls.
        Format: error=ERROR message='...' file='...' line=...
        """
        loc = self._print_caller_info(data, as_dict=True)
        return (
            f"error={data.error_name} "
            f"message={data.message!r} "
            f"file={loc['file']!r} line={loc['line']}"
        )

    def _full_outcome(self, data: SimpleExceptionData) -> str:
        """
        Full output with all available fields.
        Format: error=ERROR message='...' value='...' file='...' line=...
        """
        loc = self._print_caller_info(data, as_dict=True)

        parts = [
            f"error={data.error_name}",
            f"message={data.message!r}" if data.message else None,
            f"value_label={data.value_label!r}" if data.value_label else None,
            f"value={self._print_value_with_type(data)!r}" if data.value is not UNSET else None,
            f"expected={data.expected!r}" if data.expected else None,
            f"problem={data.problem!r}" if data.problem else None,
            f"context={data.context!r}" if data.context else None,
            f"file={loc['file']!r} line={loc['line']}" if data.caller_info else None,
            f"how_to_fix={' | '.join(data.how_to_fix)!r}" if data.how_to_fix else None,
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
    error=ERROR message='...' value_label='...' value='...' expected='...' problem='...' context='...' file='filename.py' line=42 how_to_fix='...'

## Field order
1. `error` — the error name
2. `message` — free-form message
3. `value_label` + `value` — what was being inspected
4. `expected` + `problem` + `context` — error details
5. `file` + `line` — location
6. `how_to_fix` — remediation

## Constraints
- Multi-line fields (like `intercepted_exception`) are excluded to prevent 
  breaking the single-line integrity required by log processors.
- If `data.caller_info` is missing, location fields are omitted from the string.
"""