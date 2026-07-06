
from typing import Any
# Outers
from ....SimpleExceptionSettings import SimpleExceptionSettings as S


def process_get_location(
    value: Any,
) -> int | bool:
    """
    Processes the get_location parameter — returns the value or the settings default.

    Args:
        value: The provided value of the get_location parameter.

    Returns:
        int or bool — from the provided value, or S.GET_LOCATION.
    """
    if isinstance(value, (int, bool)):
        return value
    return S.GET_LOCATION


_DESIGN_NOTES = """
# process_get_location

## Purpose
Processes the `get_location` parameter, which controls how deep in the call
stack to search for a relevant frame when reporting the exception location.

## Logic
If the provided value is an `int` or `bool`, it is used directly.
Otherwise (including `UNSET`), `S.GET_LOCATION` from settings is used.

## Why settings and not a class-level default
Unlike other parameters (e.g. `error_name`), `get_location` has no meaningful
class-level default in `SimpleExceptionData` — its default value is managed
centrally through `SimpleExceptionSettings.GET_LOCATION`, so that
the behaviour can be changed globally for the entire ecosystem without needing
to override class-level attributes.

## Usage
Used exclusively for the `get_location` parameter in `SimpleException.__init__`.
The result is stored in `self._get_location` — a private attribute because it
is configuration for the location resolver, not exception data itself.

## Notes
- `bool` is a subtype of `int` in Python, so `isinstance(True, int)` returns
  `True`. The order of the check is therefore not critical, but `(int, bool)`
  makes the intent more explicit.
- The method never raises an exception — see the general principle of
  normalisation methods.
"""