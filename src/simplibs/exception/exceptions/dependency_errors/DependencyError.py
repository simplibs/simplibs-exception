# Inners
from ..base_error.SimpleError import SimpleError


class DependencyError(SimpleError):
    """A required dependency is missing, incompatible, or failed to load.

    General-purpose exception for problems with external dependencies —
    missing packages, incompatible versions, optional dependencies not
    installed, or a dependent simplibs library not available.
    """
    pass


_DESIGN_NOTES = """
# DependencyError

## Purpose
General-purpose exception for "a required dependency is missing, incompatible, or failed to load" —
e.g. an optional third-party package not installed, a version mismatch, or another simplibs library
that a given feature depends on not being available in the environment.

## Rationale
Kept as its own category rather than folded into `StateError` or `ConfigurationError`: a missing
dependency is neither a state problem within the object's own lifecycle nor a configuration value
supplied by the user — it's an environment/installation problem, and callers may want to react to it
distinctly (e.g. print an install hint).
"""