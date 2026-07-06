from typing import Any, TYPE_CHECKING
from simplibs.sentinels import UNSET
# Annotations
if TYPE_CHECKING:
    from ...protocols import SimpleExceptionDataProtocol


def to_dict(
    self: "SimpleExceptionDataProtocol"
) -> dict[str, Any]:
    """
    Serializes core public exception attributes into a clean dictionary.
    Omitted any unconfigured (UNSET) values, configurations, and location metadata.
    """
    # Explicit definition of public business-logic attributes
    candidates = {
        "error_name": self.error_name,
        "label": self.label,
        "message": self.message,
        "expected": self.expected,
        "value": self.value,
        "problem": self.problem,
        "context": self.context,
        "how_to_fix": self.how_to_fix,
    }

    # Filter out UNSET values dynamically
    return {key: val for key, val in candidates.items() if val is not UNSET}


_DESIGN_NOTES = """
# to_dict

## Purpose
Generates a high-level, human-focused dictionary representation of the exception's 
core payload. It is tailored for standard application logging, public API error responses, 
or upstream user feedback loops.

## Explicit Mapping Strategy
Rather than using generic runtime inspection algorithms (like `get_type_hints` or tracking 
`__dict__` keys), this function explicitly states the eligible property fields. This guarantees 
strict data isolation: internal configuration toggles (`oneline`, `get_location`) or 
computed execution frames (`caller_info`) never leak into the output payload.

## Sentinel Filtration
The extraction loop strictly filters against the global `UNSET` sentinel token. 
If a field was not explicitly provided by the developer during instantiation, it is completely 
absent from the returned dictionary, preventing messy `null` or placeholder footprints in logs.
"""