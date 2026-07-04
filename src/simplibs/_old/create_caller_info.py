from typing import Any
from simplibs.sentinels import UNSET
# Inners
from ._extract_caller_info import _extract_caller_info


def create_caller_info(
    cached_caller_info,
    get_location,
    skip_locations
):
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
    if cached_caller_info is not UNSET:
        return cached_caller_info

    # 2. If location reporting is disabled, store None and exit
    if not get_location:
        return None

    # 3. Compute information using extract_caller_info
    # _get_location acts as expected_frames (1 = first user frame)
    computed_info = _extract_caller_info(
        expected_frames=int(get_location),
        excluded_patterns=skip_locations
    )

    # 4. Cache and return
    return computed_info