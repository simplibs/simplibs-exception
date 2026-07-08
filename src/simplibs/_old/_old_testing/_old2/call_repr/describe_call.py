from typing import Any, Callable


def describe_call(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> str:
    """
    Builds a human-readable "function(args, kwargs)" string for use inside
    assertion failure messages — so a failing test immediately shows what
    was actually called, not just that "something" failed.
    """
    name = getattr(func, "__name__", repr(func))
    args_repr = ", ".join(repr(a) for a in args)
    kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
    joined = ", ".join(part for part in (args_repr, kwargs_repr) if part)
    return f"{name}({joined})"