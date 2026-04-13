import functools
from typing import Callable, Any


def raise_location_offset(offset: int = 1):
    """
    Decorator that catches an exception and adds a location offset before re-raising.

    Useful for utility/validation functions where you want the error to point
    to the caller of the utility, not the line inside the utility itself.
    """

    # 1. Define the decorator
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        # 2. Define the wrapper
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            # 2.1 Wrap the function call in a try/except block
            try:
                return func(*args, **kwargs)
            except Exception as e:

                # 2.2 Check if the exception supports offset (duck typing)
                if hasattr(e, "with_location_offset"):

                    # 2.3 Add offset and re-raise without context (from None)
                    raise e.with_location_offset(offset) from None

                # 2.4 Fallback for standard exceptions
                raise e

        # Return the wrapper
        return wrapper

    # Return the decorator
    return decorator


_DESIGN_NOTES = """
# raise_location_offset (Decorator)

## Purpose
Automates the re-targeting of exceptions within a function. It is designed 
specifically for "wrapper" or "gatekeeper" functions that perform validation 
on behalf of their callers.

## Logic
When the decorated function raises an exception, the decorator intercepts it. 
If the exception has a `with_location_offset` method, it is invoked with the 
provided offset, and the "shifted" exception is raised.

## Context Management
Uses `from None` to suppress the original exception context. This ensures the 
traceback is clean and doesn't show the "During handling of the above exception..." 
message, which would be confusing when we are intentionally re-targeting the origin.

## Why Duck Typing
Similar to `raise_with_location_offset`, we use `hasattr(e, "with_location_offset")` 
instead of `isinstance(e, SimpleException)`. This prevents circular 
dependencies between the `tools` and `SimpleException` modules and allows 
the decorator to work with any future exception classes that implement the offset 
protocol.
"""