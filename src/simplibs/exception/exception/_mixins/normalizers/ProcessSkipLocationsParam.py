from simplibs.sentinels import UnsetType
# Outers
from ....settings import SimpleExceptionSettings as S


# noinspection PyMethodMayBeStatic
class ProcessSkipLocationsParamMixin:
    """Mixin for processing the skip_locations parameter."""

    def _process_skip_locations_param(
        self,
        value: tuple[str, ...] | list[str] | str | UnsetType,
    ) -> tuple[str, ...]:
        """
        Processes the skip_locations parameter and merges it with the global blacklist.

        Args:
            value: The provided value of the skip_locations parameter.

        Returns:
            tuple[str, ...] — a merge of the provided value and S.DEFAULT_LOCATION_BLACKLIST.
        """
        # 1. Normalise the provided value to tuple[str, ...]
        if isinstance(value, str):
            normalized = (value,)
        elif isinstance(value, (tuple, list)):
            strings = [i for i in value if isinstance(i, str)]
            normalized = tuple(strings) if strings else ()
        else:
            normalized = ()

        # 2. Merge with the global blacklist from settings
        return normalized + S.DEFAULT_LOCATION_BLACKLIST


_DESIGN_NOTES = """
# ProcessSkipLocationsParamMixin

## Purpose
Processes the `skip_locations` parameter, which defines file name patterns
that should be skipped when searching for a relevant frame in the call stack.

## Logic
1. **Input normalisation** — a `str`, `tuple[str]`, or `list[str]` is
   normalised to `tuple[str, ...]`. An absent value (`UNSET`, `None`, or
   an empty collection) is normalised to an empty tuple `()`.
2. **Merge with the blacklist** — the normalised value is always merged with
   `S.DEFAULT_LOCATION_BLACKLIST` from settings. This guarantees that the
   global blacklist is always present, regardless of what the user provided.

## Why the merge happens here
Merging with `DEFAULT_LOCATION_BLACKLIST` belongs in this method because it
is an inseparable part of processing this parameter — the resulting tuple
must always contain both. Doing the merge in `__init__` would split the logic
across two places.

## Usage
Used exclusively for the `skip_locations` parameter in `SimpleException.__init__`.
The result is stored in `self._skip_locations` — a private attribute because
it is configuration for the location resolver, not exception data itself.

## Notes
- An empty tuple `()` is a valid result — it means only the files from the
  global blacklist are skipped.
- The method never raises an exception — see the general principle of
  normalisation methods.
"""