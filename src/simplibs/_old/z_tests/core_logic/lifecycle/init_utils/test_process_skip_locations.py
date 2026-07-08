from typing import TYPE_CHECKING, Any
# Outers
from ....SimpleExceptionSettings import SimpleExceptionSettings as S
# Inners
from .normalize_strings import normalize_strings
# Annotations
if TYPE_CHECKING:
    from ....protocols import SimpleExceptionDataProtocol


def process_skip_locations(
    instance: "SimpleExceptionDataProtocol",
    value: Any,
) -> tuple[str, ...]:
    """Processes the skip_locations parameter, normalizes it via normalize_strings,

    and merges it sequentially with the global user blacklist and system protected frames.
    """
    # 1. Normalize local input using our standard string collection normalizer
    normalized = normalize_strings(instance, value, "skip_locations") or ()

    # 2. Merge sequentially: local overrides + user global blacklists + system core filters
    # noinspection PyProtectedMember
    return normalized + S.LOCATION_BLACKLIST + S._SYSTEM_BLACKLIST


_DESIGN_NOTES = """
# process_skip_locations

## Purpose
Processes and consolidates the `skip_locations` instance attribute into a single, comprehensive, 
and authoritative blacklist matrix used during stack trace traversal.

## Sequential Compilation Strategy
The function serves as the definitive architecture point where all framework filtering layers 
converge. It merges the array sequences in a specific order designed to optimize short-circuit 
evaluation during stack traversal:

1. **Instance-Level Noise (`normalized`)**: Local configurations passed directly to the exception 
   constructor. These represent the most context-specific filters.
2. **Global User Blacklist (`S.LOCATION_BLACKLIST`)**: Application-wide shared architectural filters 
   defined by the developer inside the settings registry.
3. **System Protected Frames (`S._SYSTEM_BLACKLIST`)**: Immutable, core-level infrastructure boundaries 
   (such as virtual interpreter markers `"<"` and the library's own package path).

## Architectural Value
By embedding `_SYSTEM_BLACKLIST` directly into the computed instance attribute, the downstream 
trace engine (`extract_caller_info`) is completely decoupled from the settings layer. It treats 
`skip_locations` as the single, fully compiled source of truth, optimizing execution speed and 
simplifying package interaction boundaries.
"""