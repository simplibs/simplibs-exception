# Inners
from ..base_error.SimpleError import SimpleError


class StateError(SimpleError):
    """An object or system is not in the state a given operation requires.

    Root of the state-related exception family. Raised when an operation was
    attempted while its preconditions about current state were not met. More
    specific state contexts (e.g. missing initialization, invalid
    configuration) should subclass this rather than being raised directly.
    """
    pass


_DESIGN_NOTES = """
# StateError

## Purpose
General-purpose exception for "an object or system is not in the state a
given operation requires". This is the parent for every more specific state
scenario (currently: `InitializationError`, `ConfigurationError`).

## Scope
Raise `StateError` directly only when the situation is a genuine state
mismatch that isn't specifically about initialization or configuration
(e.g. calling a method after an object has already been closed/consumed).
If the problem is that something was never initialized, raise
`InitializationError`; if it's about invalid/missing configuration, raise
`ConfigurationError` instead, so callers can distinguish between the two
common causes and the general case.
"""