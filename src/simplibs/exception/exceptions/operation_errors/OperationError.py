# Inners
from ..base_error.SimpleError import SimpleError


class OperationError(SimpleError):
    """A runtime operation or process failed while executing.

    General-purpose exception for "something failed while it was running" —
    as opposed to failing validation up front (`ValidationError`) or failing
    because of preconditions about state (`StateError`).
    """
    pass


_DESIGN_NOTES = """
# OperationError

## Purpose
General-purpose exception for "a runtime operation or process failed while it was executing" —
covering what would otherwise have been split across `OperationError`/`ProcessError`/`RunningError`.

## Rationale
`ProcessError` was folded into this class — the two were effectively synonyms ("an operation/process
failed at runtime") and keeping them separate offered no meaningful distinction for callers to catch
differently. `RunningError` was deliberately left out for now: its candidate meanings ("already
running" -> a state conflict, arguably `StateError`; or "failed while running" -> exactly this class)
both already have a home. It can be reintroduced later as a genuine subclass if a concrete use case
emerges that neither `OperationError` nor `StateError` covers.
"""