from typing import Any


def is_raise_function(
    item: Any
) -> bool:
    """
    Return True if item is a tuple of:
        (exception_class, function)
    where function takes no parameters.
    """
    if not isinstance(item, tuple):
        return False
    if len(item) != 2:
        return False

    exc_class, func = item
    return (
        isinstance(exc_class, type)
        and issubclass(exc_class, BaseException)
        and callable(func)
    )