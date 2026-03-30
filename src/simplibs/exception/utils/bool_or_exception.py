def bool_or_exception(return_bool: bool, **kwargs) -> bool:
    """Returns False or raises SimpleException — a shortcut for conditional exception raising."""

    # 1. Return False if a bool return is requested
    if return_bool:
        return False

    # 2. Offset the location value to account for this file
    get_location = kwargs.get("get_location")
    if isinstance(get_location, int) and get_location > 0:
        kwargs["get_location"] = get_location + 1

    # 3. Raise the exception
    from ..exception.SimpleException import SimpleException
    raise SimpleException(**kwargs)


_DESIGN_NOTES = """
# bool_or_exception

## Purpose
A shortcut for the pattern where a function either returns `False` or raises
a `SimpleException`. Intended for use where a `return_bool` parameter exists —
a flag that controls whether to return `False` on failure instead of raising.

## Pattern it replaces
    # Without bool_or_exception:
    if not is_valid:
        if return_bool:
            return False
        raise SimpleException(
            value_label = "parameter age",
            expected    = "positive integer",
        )
    return False

    # With bool_or_exception:
    return bool_or_exception(
        return_bool,
        value_label = "parameter age",
        expected    = "positive integer",
    )

## Why SimpleException is imported inside the function
`bool_or_exception` lives in `utils` — and `utils` is a dependency of
`SimpleException` (sentinel, extract_caller_info). Importing `SimpleException`
at module level would create a circular dependency:

    utils/__init__.py
      → exception_helper/bool_or_exception.py
        → exception/SimpleException.py
          → core/SimpleExceptionData.py
            → utils/__init__.py  ← cycle

A lazy import inside the function breaks this cycle — `SimpleException` is
loaded only on the first call, by which point all modules are fully initialised.
This is an intentional architectural decision, not a workaround.

## Notes
- `return_bool=True`  → the function returns `False` without raising.
- `return_bool=False` → the function raises `SimpleException` with the provided kwargs.
- `get_location` is automatically incremented by 1 — so the reported location
  points to the call site of `bool_or_exception`, not to this function itself.
- All `**kwargs` are passed directly to `SimpleException.__init__`.
- This function is a convenience helper — it is not required for the ecosystem to work.
"""