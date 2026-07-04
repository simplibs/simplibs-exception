from typing import Any, TYPE_CHECKING
from inspect import isclass
from simplibs.sentinels import UNSET, UnsetType
if TYPE_CHECKING:
    from ...protocols import SimpleExceptionProtocol


def process_exception_param(
    instance: object,
    exception: Exception | type[Exception] | UnsetType,
) -> tuple[type[Exception] | UnsetType, str | UnsetType]:

    # 1. Fall back to the class-level default if nothing was provided
    if exception is UNSET:
        exception = instance.__class__.exception

    # 2. Process an Exception-based class
    if isclass(exception) and issubclass(exception, Exception):
        return exception, UNSET

    # 3. Process an exception instance (e.g. passed as e from an except block)
    if isinstance(exception, Exception):
        return type(exception), str(exception) or UNSET

    # 4. Fallback for invalid or absent input
    return UNSET, UNSET


_DESIGN_NOTES = """
# ProcessExceptionParamMixin

## Purpose
Processes the `exception` parameter, which may be provided as an exception
class or as an exception instance, and normalises it into a consistent output
format.

## Logic
1. **Class-level default** — if no value was provided (`UNSET`), the method
   first attempts to load the class attribute `exception` from `self.__class__`.
   This keeps behaviour consistent with other normalisation methods that also
   resolve their fallback internally via `getattr(self.__class__, attr)`,
   so the calling code in `__init__` does not need to handle this logic itself.
2. **Exception class** (`ValueError`, `TypeError`, ...) — returns the class and
   `UNSET` as the description, since a class by itself carries no description.
3. **Exception instance** (`ValueError("message")`) — returns the type of the
   instance and its string representation as the description. If the string is
   empty, returns `UNSET`.
4. **Anything else** (UNSET, None, a number, ...) — returns `(UNSET, UNSET)`,
   meaning no exception was provided.

## Output values and UNSET
Both elements of the output tuple use `UNSET` to represent an absent value —
consistent with the other optional parameters in `SimpleExceptionData`.
An empty string `""` is deliberately not accepted as a description —
`str(value) or UNSET` ensures that an empty string is converted to `UNSET`.

## Usage
Used exclusively for the `exception` parameter in `SimpleException.__init__`.
The output is unpacked into two attributes:
- `self.exception` — the exception type added to the ancestors via `DunderNewMixin`
- `self._intercepted_exception` — the original message of the caught exception,
  displayed as supplementary information below the main output in modes that
  support it

## Notes
- The method never raises an exception — see the general principle of
  normalisation methods.
- Marked `# noinspection PyMethodMayBeStatic` because it technically does not
  use `self`, but as a mixin method it must take this form.
- The `exception` attribute in `SimpleExceptionData` has the type
  `type[Exception] | UnsetType = UNSET` — the output of this method is
  therefore directly compatible with that attribute.
"""