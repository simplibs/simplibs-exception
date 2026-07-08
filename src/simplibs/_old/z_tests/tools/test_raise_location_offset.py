import functools
from typing import Any, Callable


def raise_location_offset(
    offset: int = 1
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator that catches an exception and adds a location offset before re-raising.

    Useful for utility, gatekeeper, or validation functions where you want the terminal
    diagnostic report to point directly to the caller of the utility, not the line inside
    the utility itself.
    """

    # 1. Define the decorator boundary layer receiving the target function blueprint
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        # 2. Define the execution wrapper conserving the original signature metadata
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            # 2.1 Enclose execution within a defensive evaluation block
            try:
                return func(*args, **kwargs)
            except Exception as e:

                # 2.2 Evaluate via runtime duck-typing whether the exception supports frame shifting
                if hasattr(e, "with_location_offset"):
                    # 2.3 Add relative offset and re-raise suppressing local execution context
                    raise e.with_location_offset(offset) from None

                # 2.4 Resilient fallback for native standard exceptions (e.g. ValueError).
                # Using 'from None' isolates the original traceback graph from being overwritten.
                raise e from None

        # Return the configured wrapper
        return wrapper

    # Return the structural decorator
    return decorator


_DESIGN_NOTES = """
# raise_location_offset (Decorator)

## Purpose
An Aspect-Oriented Programming (AOP) declarative macro utility that automates stack-frame re-targeting. 
It converts any standard function into a transparent "gatekeeper" boundary line, shifting the reported 
failure origin back to the client call-site.

## Execution Matrix & Context Suppression
When a decorated function throws an exception, the wrapper intercepts the bubbling signal. If the 
exception instance exposes a `with_location_offset` method via structural duck-typing, it applies 
the configured relative integer offset. 

The subsequent execution phase utilizes explicit `raise ... from None` semantics. This strictly suppresses 
the internal wrapper frame context allocation inside the interpreter, ensuring that terminal terminal reports 
remain entirely clean and skip any intermediary decoration mechanics.

## Native Exception Traceback Immunity
If the underlying execution throws a primitive native exception (such as an internal `IndexError`), the 
interceptor steps back into a passive passthrough state. Forcing `raise e from None` guarantees that the 
core Python interpreter re-emits the original error structure without polluting or truncating its native 
origin traceback graph.
"""