from simplibs.sentinels import UnsetType


class ProcessHowToFixParamMixin:
    """Mixin for processing the how_to_fix parameter."""

    def _process_how_to_fix_param(
        self,
        value: tuple[str, ...] | str | UnsetType,
    ) -> tuple[str, ...] | UnsetType:
        """
        Processes the how_to_fix parameter — normalises to tuple[str, ...] or returns the class-level default.

        Args:
            value: The provided value of the how_to_fix parameter.

        Returns:
            tuple[str, ...] — from the provided value, or the class-level default of how_to_fix.
        """
        # 1. Process a string
        if isinstance(value, str):
            return (value,)

        # 2. Process a tuple or list — retains only str items
        if isinstance(value, (tuple, list)):
            strings = [i for i in value if isinstance(i, str)]
            if strings:
                return tuple(strings)

        # 3. Fall back to the class-level default
        return getattr(self.__class__, "how_to_fix")


_DESIGN_NOTES = """
# ProcessHowToFixParamMixin

## Purpose
Processes the `how_to_fix` parameter, which may be provided as a `str`,
`tuple[str, ...]`, or `list[str]`, and normalises it to the consistent
output type `tuple[str, ...]`.

## Logic
1. If a `str` is provided — wraps it in a tuple. The most common case,
   where the user passes a single tip as a plain string.
2. If a `tuple` or `list` is provided — retains only `str` items and
   silently filters out the rest. If any items remain after filtering,
   returns them as a tuple.
3. In all other cases (UNSET, None, invalid type, empty collection) —
   the class-level default from `self.__class__.how_to_fix` is used,
   following the same principle as the other normalisation methods.

## Why lists are also accepted
The `how_to_fix` parameter is annotated as `tuple[str, ...] | str` —
a list is therefore not an officially supported type. Internal list support
is an intentional convenience: lists and tuples are structurally equivalent
collections, and passing a list is not an error in any logical sense.

### Note on parameter annotation
A list is intentionally excluded from the annotation — for the following reasons:
- A tuple signals immutability, which is the correct semantics for this parameter.
- Including a list in the annotation would expand the public interface without
  a real need.
- Silent internal support for lists is a gentle nudge — it works, but the user
  is guided towards passing a tuple.

The annotation therefore remains:
    how_to_fix: tuple[str, ...] | str | UnsetType = UNSET

## Usage
Used exclusively for the `how_to_fix` parameter in `SimpleException.__init__`.
The result is stored in `self.how_to_fix` — a public attribute because it is
part of the exception description displayed in the output.

## Notes
- An empty collection falls through to the fallback (step 3) — an empty tuple
  is therefore never returned; the result is always either a non-empty tuple
  or the class-level default.
- The method never raises an exception — see the general principle of
  normalisation methods.
"""