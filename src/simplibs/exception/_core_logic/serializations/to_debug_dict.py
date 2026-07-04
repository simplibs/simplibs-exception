from typing import Any, TYPE_CHECKING
# Inners
from .to_dict import to_dict
# Annotations
if TYPE_CHECKING:
    from ...protocols import SimpleExceptionDataProtocol


def to_debug_dict(
    self: "SimpleExceptionDataProtocol"
) -> dict[str, Any]:
    """
    Compiles a comprehensive diagnostic snapshot dictionary for developers.
    Extends standard data with fully realized runtime frames and rendered outputs.
    """
    # 1. Establish foundation using the standard public serialization
    result = to_dict(self)

    # 2. Inject lazy-loaded, structural location footprint metadata
    # (Extracts file, path, line, function from the dynamic execution context)
    if self.caller_info:
        result["caller_info"] = self.caller_info

    # 3. Inject underlying intercepted trace summaries if active
    if self.intercepted_exception:
        result["intercepted_exception"] = self.intercepted_exception

    # 4. Inject the absolute compiled console layout output representation string
    # (Safe-guarding via getattr in case serialization executes pre-initialization)
    rendered_msg = getattr(self, "rendered_message", None)
    if rendered_msg:
        result["rendered_message"] = rendered_msg

    return result


_DESIGN_NOTES = """
# to_debug_dict

## Purpose
Assembles a dense, low-level inspection state dictionary intended strictly for 
internal engineering diagnostic backends, telemetry tools (e.g., Sentry), or 
crash dump storage.

## Extended Composition Pattern
To maintain architectural symmetry and zero data duplication, `to_debug_dict` 
directly invokes `to_dict(self)` as its foundation layout block. It then wraps 
and injects complex internal runtime calculations:
- **caller_info**: Flattens the dynamically resolved filesystem trace dictionary.
- **intercepted_exception**: Identifies the caught class type name that initialized the failure chain.
- **rendered_message**: Stores the exact visual terminal text copy block seen by the operator.

## Defensive Attribute Fetching
The function reads `rendered_message` using `getattr(self, "rendered_message", None)`. 
This acts as a defensive guard. If an exception state is audited during an early step 
of its construction phase (before the final message compilation runs), the snapshot 
engine resolves gracefully without triggering an unexpected `AttributeError`.
"""