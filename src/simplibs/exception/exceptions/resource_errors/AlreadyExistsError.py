# Inners
from .ResourceError import ResourceError


class AlreadyExistsError(ResourceError):
    """A resource could not be created because it already exists.

    Specialization of `ResourceError` and the direct counterpart to
    `NotFoundError` — raised on creation/insertion conflicts rather than
    on lookups.
    """
    pass


_DESIGN_NOTES = """
# AlreadyExistsError

## Purpose
Specialization of `ResourceError` for the case where an operation tried to create or register a
resource (file, DB row, cache key, registry entry, ...) under an identifier that is already taken.

## Rationale
Direct counterpart to `NotFoundError` — together they cover both ends of "does this identifier
already have something behind it". Kept separate from `NotFoundError` rather than a single toggled
exception so callers can `except` each conflict type independently.
"""