from typing import Any


def manage_param(
    param: Any,
) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """Normalize a raw parameter definition into ``args`` and ``kwargs``."""

    # 1. Explicit kwargs wrapper
    if isinstance(param, Kwargs):
        return (), dict(param.values)

    # 2. Multiple positional arguments
    if isinstance(param, (tuple, list)):
        if not param:
            return (param,), {}

        if isinstance(param[-1], Kwargs):
            return (
                tuple(param[:-1]),
                dict(param[-1].values),
            )

        return tuple(param), {}

    # 3. Single positional argument
    return (param,), {}