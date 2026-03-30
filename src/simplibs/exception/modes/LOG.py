from simplibs.sentinels import UNSET
# Commons
from ..core import SimpleExceptionData
# Inners
from .base_class import ModeBase


# noinspection PyProtectedMember
class LogMessage(ModeBase):
    """Structured key=value output for log parsers."""

    def _empty_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """
        Output for a call with no data at all.

        error=ERROR file='...' line=...
        """
        loc = self._print_caller_info(caller_info, as_dict=True)
        return f"error={data.error_name} file={loc['file']!r} line={loc['line']}"

    def _message_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """
        Output for message-only calls.

        error=ERROR message='...' file='...' line=...
        """
        loc = self._print_caller_info(caller_info, as_dict=True)
        return (
            f"error={data.error_name} "
            f"message={data.message!r} "
            f"file={loc['file']!r} line={loc['line']}"
        )

    def _full_outcome(self, data: SimpleExceptionData, caller_info: dict | None) -> str:
        """
        Full output with all available fields.

        error=ERROR message='...' value_label='...' value='...' expected='...' problem='...' context='...' file='...' line=... how_to_fix='...'
        """
        loc = self._print_caller_info(caller_info, as_dict=True)
        parts = [
            f"error={data.error_name}",
            f"message={data.message!r}"                     if data.message else None,
            f"value_label={data.value_label!r}"             if data.value_label else None,
            f"value={self._print_value_with_type(data)!r}"  if data.value is not UNSET else None,
            f"expected={data.expected!r}"                   if data.expected else None,
            f"problem={data.problem!r}"                     if data.problem else None,
            f"context={data.context!r}"                     if data.context else None,
            f"file={loc['file']!r} line={loc['line']}"      if caller_info else None,
            f"how_to_fix={' | '.join(data.how_to_fix)!r}"   if data.how_to_fix else None,
        ]
        return " ".join(part for part in parts if part)


# Singleton mode instance
LOG = LogMessage()


_DESIGN_NOTES = """
# LOG

## Purpose
Output in `key=value` format (logfmt) — designed for machine processing by
log parsers. Each field is explicitly named and space-separated.
Suited for production environments where logs are processed by an external
tool (e.g. Elasticsearch, Datadog, Splunk).

Unlike `PRETTY` and `SIMPLE`, it contains no visual decoration —
the output is a plain string intended to be read by machines, not humans.

## Output scenarios

### Empty call
    error=ERROR file='filename.py' line=42

### Message only
    error=ERROR message='...' file='filename.py' line=42

### Full output
    error=ERROR message='...' value_label='...' value='...' expected='...' problem='...' context='...' file='filename.py' line=42 how_to_fix='...'

## Field order
Fields are ordered from most to least important:
1. `error` — always present, the error name
2. `message` — free-form message, equivalent to a classic Exception("text")
3. `value_label` + `value` — what was being inspected
4. `expected` + `problem` + `context` — description of the error
5. `file` + `line` — location (only if caller_info is available)
6. `how_to_fix` — remediation

## caller_info
Passed as a parameter from `render_message` in `ModeBase`. LOG mode uses
`_print_caller_info(caller_info, as_dict=True)` to obtain raw data and
assemble its own `file=... line=...` format instead of a pre-formatted string.
If `caller_info` is None, the `file` and `line` fields are not included.

## intercepted_exception
LOG mode intentionally does not include `intercepted_exception` — it is
multi-line text that would break the `key=value` format and make machine
processing significantly harder.

## Singleton
The class is used exclusively through the `LOG` instance — the mode is
stateless, so there is no reason to create multiple instances.
"""