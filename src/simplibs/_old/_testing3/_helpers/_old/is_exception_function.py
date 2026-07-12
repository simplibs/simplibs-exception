from typing import Any
# Inners
from .is_exception_class import is_exception_class


def is_exception_function(
    item: Any
) -> bool:
    """Determine whether the item matches the functional testing tuple footprint.

    Returns True if the item is a sequence (tuple) whose first element is a valid
    exception class and whose second element is an executable callable object.
    """
    if not isinstance(item, tuple) or len(item) < 2:
        return False

    exc_cls, function = item[0], item[1]

    # Verify that the sequence header conforms to an exception blueprint and an executable function
    is_valid_class = is_exception_class(exc_cls)
    is_callable = callable(function)

    return is_valid_class and is_callable


_DESIGN_NOTES = """
# is_exception_function (Functional Sequence Router)

## Purpose
An internal introspection helper designed to recognize validation-wrapper signatures. It screens input 
items to detect sequence layouts indicating that a callable function target is being subjected to automated 
exception intercept validations.

## Expected Signatures Footprint
The guard verifies compliance against the following multi-parameter tuple conventions:
- `(exception_class, validation_function)`
- `(exception_class, validation_function, *positional_args)`

It carefully inspects individual structural markers—ensuring index `0` holds a compliant `BaseException` 
blueprint type, and index `1` maps to an executable routine (`callable`)—before giving green light 
to down-stream `pytest.raises` test layers.
"""