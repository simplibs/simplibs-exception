# Inners
from .StateError import StateError


class ConfigurationError(StateError):
    """Required configuration is missing or invalid.

    Specialization of `StateError` scoped specifically to configuration —
    as opposed to runtime state problems arising from normal object usage.
    """
    pass


_DESIGN_NOTES = """
# ConfigurationError

## Purpose
Specialization of `StateError` for the case where a system's configuration
is missing, incomplete, or invalid (e.g. a required setting not set, an
environment variable missing, an incompatible combination of settings).

## Rationale
Configuration problems are a distinct, very common failure mode — distinct
from both "not initialized yet" (`InitializationError`) and general runtime
state mismatches (`StateError`). Giving it its own subclass lets callers
(and operators reading logs) immediately recognize a deployment/setup issue
rather than a code-level bug.
"""