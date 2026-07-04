from typing import Any
from simplibs.sentinels import UNSET
# Inners
from .utils import extract_caller_info


class CallerInfoMixin:
    """Mixin providing the lazily-computed caller_info property."""

    # Expects (Duck Typing):
    _cached_caller_info: Any
    _get_location: int | bool
    _skip_locations: tuple[str, ...]

    @property
    def caller_info(self) -> dict[str, Any] | None:
        """
        Lazily-computed and cached call site information.

        Returns:
            Dictionary with keys: file, full_path, line, function
            Or None if location reporting is disabled or frame not found.

        Caching:
            Computes only once — result is cached in _cached_caller_info.
            Subsequent accesses return the cached value immediately.
        """
        # 1. If already computed, return the cached value
        if self._cached_caller_info is not UNSET:
            return self._cached_caller_info

        # 2. If location reporting is disabled, store None and exit
        if not self._get_location:
            self._cached_caller_info = None
            return None

        # 3. Compute information using extract_caller_info
        # _get_location acts as expected_frames (1 = first user frame)
        computed_info = extract_caller_info(
            expected_frames=int(self._get_location),
            excluded_patterns=self._skip_locations
        )

        # 4. Cache and return
        self._cached_caller_info = computed_info
        return computed_info


_DESIGN_NOTES = """
# CallerInfoMixin

## Purpose
Provides a property for lazy retrieval of the exception's origin. Attached 
to the data layer, it makes all exceptions "location-aware" without 
polluting the core exception logic.

## Lazy Evaluation & Caching
Introspection is expensive. We only perform `extract_caller_info` when 
`caller_info` is actually accessed. The result is cached in 
`_cached_caller_info` to prevent repeated stack traces during multiple 
outputs (e.g., logging and CLI display).

## The Selection Logic (New)
The mixin now relies on the content-based filtering of `extract_caller_info`:
- **No manual offsets:** We no longer use `depth + 1`. The introspection 
  utility automatically skips library-internal frames based on path 
  patterns.
- **Expected Frames:** `_get_location` (if it's an int) directly represents 
  the N-th valid user frame. 
- **Decoupling:** This makes the mixin immune to the internal structure of 
  the library. Even if we add more helper layers, `expected_frames=1` will 
  still point to the user's code.

## Implementation Details
- **Architecture:** Foundational property for the `simplibs` ecosystem.
- **Duck Typing:** Interacts with attributes of the class it's mixed into 
  without strict inheritance requirements.
- **Fallout Safety:** If `extract_caller_info` fails to find the exact 
  frame, its internal fallout mechanism ensures we still get the most 
  relevant context possible.
"""