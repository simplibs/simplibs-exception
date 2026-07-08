import json
from typing import Any, TYPE_CHECKING
from dataclasses import dataclass
from simplibs.sentinels import UNSET, UnsetType
# Inners
from .core_logic.tracing import extract_caller_info
from .core_logic.serializations import to_dict as _to_dict
from .core_logic.serializations import to_debug_dict as _to_debug_dict
# Annotations
if TYPE_CHECKING:
    from .protocols import SimpleExceptionDataProtocol


@dataclass
class SimpleExceptionData:
    """Pure state data class defining the attributes, boundaries, and defaults of SimpleException."""

    # --- Core exception info ---
    error_name: str = "ERROR"
    exception: type[Exception] | None = None
    intercepted_exception: str | None = None

    # --- Info about the inspected value ---
    # The sentinel MUST remain here because the value can literally be anything (including None)
    value: Any = UNSET

    # --- Exception description ---
    label: str | None = None
    expected: str | None = None
    message: str | None = None
    problem: str | tuple[str, ...] | None = None
    context: str | tuple[str, ...] | None = None

    # --- How to fix ---
    how_to_fix: str | tuple[str, ...] | None = None

    # --- Location info ---
    get_location: int | bool = True
    skip_locations: tuple[str, ...] = ()
    _cached_caller_info: dict[str, Any] | None | UnsetType = UNSET

    # --- Single-line output ---
    oneline: bool = False

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def caller_info(self) -> dict[str, Any] | None:
        """
        Lazily-computed and cached filesystem call site metadata footprint.

        Returns:
            Dictionary containing structured keys: file, path, line, function.
            Returns None if location reporting is disabled or the execution frame is missing.

        Caching Strategy:
            Evaluates exactly once. The outcome is locked inside _cached_caller_info.
            Subsequent access pulls from the state cache instantly with zero overhead.
        """
        # 1. Immediately short-circuit if the consumer explicitly muted tracking
        if not self.get_location:
            return None

        # 2. Execute heavy stack introspection only if the cache has never been filled
        if self._cached_caller_info is UNSET:
            # get_location acts as expected_frames (1 = immediate user boundary frame)
            self._cached_caller_info = extract_caller_info(
                expected_frames=int(self.get_location),
                excluded_patterns=self.skip_locations,
            )

        # 3. Return the structurally validated cache layer dict or None footprint
        # noinspection PyTypeChecker
        return self._cached_caller_info

    # -------------------------------------------------------------------------
    # Serializers
    # -------------------------------------------------------------------------

    def to_dict(self: "SimpleExceptionDataProtocol") -> dict[str, Any]:
        """Serializes core public exception attributes into a clean dictionary — UNSET values are omitted."""
        return _to_dict(self)

    def to_debug_dict(self: "SimpleExceptionDataProtocol") -> dict[str, Any]:
        """Compiles a comprehensive diagnostic snapshot dictionary including computed metadata."""
        return _to_debug_dict(self)

    def to_json(self: "SimpleExceptionDataProtocol") -> str:
        """Serializes core instance public data fields into an un-indented JSON string representation."""
        return json.dumps(self.to_dict(), default=str)


_DESIGN_NOTES = """
# SimpleExceptionData

## Purpose
Acts as the decoupled, pure state storage layer for the `SimpleException` architecture. 
It defines the baseline data attribute constraints, defaults, and serializations, 
serving as the absolute single source of truth across the entire application ecosystem. 
It completely isolates error data parameters from text formatting, layout engines, or runtime MRO shifts.

## Location Awareness & Clean Delegations
Rather than spreading frame extraction mixins throughout the library, `SimpleExceptionData` 
encapsulates call-site tracing inside a lazy `@property def caller_info`:
1. **Lazy Evaluation Pipeline**: Stack tracing is a computationally intensive action. The internal cache 
   (`_cached_caller_info`) remains `UNSET` until a renderer explicitly requests location data.
2. **Defensive Caching**: If the stack scanner fails or yields no frames, `None` is explicitly cached 
   as a valid state. This prevents subsequent resource leaks or repeated redundant stack iterations.
3. **Standalone Extraction**: The property orchestrates state and cache, but delegates raw frame inspection 
   directly to the decoupled `extract_caller_info()` utility function.

## Naming Conventions
- **Public Attributes (No Underscore Prefix)**: Diagnostic payload data fields intended for end-user view, 
  rendering presentation strategies, and public analytics dictionary exporters.
- **Private Attributes (Underscore Prefix)**: Internal library mechanics managed completely automatically 
  by the core engine (such as the performance caching field).

## Attribute Matrix Reference

### Core Metadata
| Attribute               | Default   | Description                                                           |
|-------------------------|-----------|-----------------------------------------------------------------------|
| `error_name`            | `"ERROR"` | High-level string category tag emitted in the visual header banner    |
| `exception`             | `None`    | Raw exception class wrapper used for structural dynamic MRO injection |
| `intercepted_exception` | `None`    | Textual identifier snapshot representing an underlying caught failure  |

### Inspected Payload Value
| Attribute | Default | Description                                                                         |
|-----------|---------|-------------------------------------------------------------------------------------|
| `value`   | `UNSET` | The live dynamic runtime object inspected; handles `None` natively via `UNSET` token|

### Diagnostic Descriptions
| Attribute  | Default | Description                                                                       |
|------------|---------|-----------------------------------------------------------------------------------|
| `label`    | `None`  | Explanatory context identifier tag for the inspected value (e.g., `"user_id"`)     |
| `expected` | `None`  | Specification constraint description detailing what state was anticipated         |
| `problem`  | `None`  | Hybrid tuple or flat string tracking exactly what validation boundary broke       |
| `context`  | `None`  | Supplementary environment metadata matrix string blocks (IPs, hashes, query IDs)  |
| `message`  | `None`  | Flat human narrative block that overrides structural layout fields if populated   |

### Actionable Remediation
| Attribute    | Default | Description                                                                     |
|--------------|---------|---------------------------------------------------------------------------------|
| `how_to_fix` | `None`  | Hybrid tuple or flat string instructions formatted into actionable bullet lists |

### Location Trace Options
| Attribute             | Default | Description                                                                        |
|-----------------------|---------|------------------------------------------------------------------------------------|
| `get_location`        | `True`  | Activation flag or custom depth offset integer guiding the stack frame lookup loop|
| `skip_locations`      | `()`    | Filepath patterns or framework modules to filter out during execution traceback scanning|
| `_cached_caller_info` | `UNSET` | Low-level storage slot backing the lazy location metadata evaluation lifecycle     |

### Layout Overrides
| Attribute | Default | Description                                                                    |
|-----------|---------|--------------------------------------------------------------------------------|
| `oneline` | `False` | Formatting hint signal directing the exception to output a single dense row   |

## Interface Specifications
This dataclass structurally satisfies `SimpleExceptionDataProtocol`. By shifting standard `to_dict()`, 
`to_debug_dict()`, and `to_json()` pipelines here, the business data remains completely isolated 
and testable independent of active Python control-flow execution structures.
"""