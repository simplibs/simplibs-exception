from inspect import isclass
from typing import Any


def print_intercepted_exception(
    exception: Any,
    *,
    prefix: str = "Intercepted exception",
    _log_mode: bool = False
) -> str | None:
    """
    Renders information about the caught exception if available.
    Skipped in log mode to prevent massive cluttered logs.
    """
    # Pokud žádná výjimka není, nemáme co tisknout
    if not exception or exception is UNSET:
        return None

    # V log módu chycené výjimky prozatím ignorujeme (nechceme obří texty v logu)
    if _log_mode:
        return None

    # 1. Scénář: Je to instance výjimky (např. except VaueError as e)
    if isinstance(exception, Exception):
        err_type = exception.__class__.__name__
        err_msg = str(exception)

        # Pokud má výjimka i textovou zprávu, vypíšeme ji pod to
        if err_msg:
            return f"{prefix} ({err_type}):\n    {err_msg}"
        return f"{prefix} ({err_type})"

    # 2. Scénář: Je to jen samotná třída výjimky (např. exception=ValueError)
    if isclass(exception) and issubclass(exception, Exception):
        return f"{prefix} ({exception.__name__})"

    return None