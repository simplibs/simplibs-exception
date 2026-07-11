from typing import Any, TypeGuard


def is_exception_class(item: Any) -> TypeGuard[type[BaseException]]:
    """Determine whether the evaluated item is a concrete exception class blueprint.

    Returns True if the item represents a raw class type derived from BaseException,
    allowing downstream pipeline routing blocks to apply structural subtype operations safely.
    """
    return isinstance(item, type) and issubclass(item, BaseException)


_DESIGN_NOTES = """
# is_exception_class (Structural Type Guard)

## Purpose
An internal introspection helper acting as a Type Guard for structural routing. It safely determines 
whether an anonymous runtime item is a class reference originating from Python's root `BaseException` hierarchy.

## Architectural Value
By leveraging a strict compile-time `TypeGuard`, it instructs static analysis tools and IDE tokenizers 
that upon a `True` confirmation, the item can be treated natively as an exception constructor. This prevents 
unwanted `TypeError` crashes inside the bulk engine before invoking reflection checks or structural scans.
"""