# Inners
from ..base_error.SimpleError import SimpleError


class ResourceError(SimpleError):
    """A problem occurred while working with an identifiable resource.

    Root of the resource-related exception family. Covers any operation
    against something addressable and identifiable — a file, a database
    record, a cache key, an API entity — regardless of storage backend.
    More specific resource contexts (not found, already exists, access
    denied) should subclass this rather than being raised directly.
    """
    pass


_DESIGN_NOTES = """
# ResourceError

## Purpose
General-purpose exception for "something went wrong while working with an identifiable resource".
This is the parent for every more specific resource scenario (currently: `NotFoundError`,
`AlreadyExistsError`, `AccessError`).

## Scope
Deliberately backend-agnostic: a "resource" here means anything addressable by an identifier —
a file path, a database row, a cache key, a remote API entity. Raise `ResourceError` directly only
when none of the more specific subclasses fit; otherwise prefer `NotFoundError`, `AlreadyExistsError`,
or `AccessError` so callers can catch the precise failure mode.
"""