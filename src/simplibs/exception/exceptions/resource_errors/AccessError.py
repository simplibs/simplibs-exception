# Inners
from .ResourceError import ResourceError


class AccessError(ResourceError):
    """A resource exists but cannot be accessed due to missing permissions or a lock.

    Specialization of `ResourceError` for permission/lock failures — as
    opposed to the resource simply not existing (`NotFoundError`).
    """
    pass


_DESIGN_NOTES = """
# AccessError

## Purpose
Specialization of `ResourceError` for the case where a resource is known to exist, but the operation
was refused — insufficient permissions, an active lock held by something else, a credential rejected.

## Rationale
Kept distinct from `NotFoundError` so callers (and operators reading logs) can immediately tell
a permissions/lock problem apart from a missing-resource problem — the remediation for each is
completely different (request access vs. create the resource).
"""