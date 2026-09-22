# Inners
from .ResourceError import ResourceError


class NotFoundError(ResourceError):
    """A requested resource does not exist.

    Specialization of `ResourceError` for lookups that came back empty —
    as opposed to lookups that failed due to permissions (`AccessError`).
    """
    pass


_DESIGN_NOTES = """
# NotFoundError

## Purpose
Specialization of `ResourceError` for the case where a lookup by identifier (file path, DB key,
cache entry, remote entity ID, ...) came back empty.

## Rationale
Distinct from `AccessError`: a `NotFoundError` means the resource genuinely does not exist (or is
indistinguishable from not existing, e.g. for security reasons an API may return 404 instead of 403).
Callers commonly want to react differently to "doesn't exist" (e.g. create it) than to "exists but
can't touch it" (e.g. request access).
"""