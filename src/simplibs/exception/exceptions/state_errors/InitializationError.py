# Inners
from .StateError import StateError


class InitializationError(StateError):
    """An object or system was used before it was properly initialized.

    Specialization of `StateError` scoped specifically to setup/bootstrap
    ordering — as opposed to state problems arising after normal use.
    """
    pass


_DESIGN_NOTES = """
# InitializationError

## Purpose
Specialization of `StateError` for the case where something is used before
its required setup/bootstrap step has completed (e.g. a resource accessed
before `.connect()`, a registry read before its entries were loaded).

## Rationale
Initialization-ordering mistakes are common enough across the simplibs
ecosystem to warrant their own subclass rather than always falling back to
the more generic `StateError`, letting callers catch this specific case
(e.g. to trigger a lazy-init retry) without also catching unrelated state
mismatches.
"""