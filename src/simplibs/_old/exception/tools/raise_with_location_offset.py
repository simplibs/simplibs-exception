from typing import NoReturn, Any


def raise_with_location_offset(
    exc: Any,
    offset: int = 1
) -> NoReturn:
    """
    Takes an exception, applies a location offset, and raises it.

    This is a helper for: raise exc.with_location_offset(offset)
    """
    # 1. Check if the exception supports offset (duck typing)
    if hasattr(exc, "with_location_offset"):
        raise exc.with_location_offset(offset)

    # 2. Fallback for standard exceptions
    raise exc


_DESIGN_NOTES = """
# raise_with_location_offset

## Purpose
A functional wrapper for the `with_location_offset` method. It allows raising 
an exception with a shifted stack trace in a single elegant call.

## Why Any and not SimpleException
To avoid circular dependencies, we don't import `SimpleException` at the 
module level. Instead, we use duck typing — if the object has the 
`with_location_offset` method, we use it. This makes the tool more robust 
and prevents import-time issues.

## Usage
Instead of:
    exc = MyError(...)
    raise exc.with_location_offset(1)

You can use:
    raise_with_location_offset(exc, 1)

This is particularly useful in catch-all blocks or decorators where you 
want to re-target the error origin to the caller of the current function.
"""