# 🧩 `SimpleExceptionData`

**The Pure State Storage Layer and Data Model for SimpleException**

The `SimpleExceptionData` class forms the structural backbone and "single source of truth" 
for the entire exception ecosystem. It completely decouples the raw exception state 
from visual formatting rules, presentation layout engines, 
and Python's dynamic runtime inheritance mechanics.

Because of this clean separation, exception state data remains highly serializable, 
testable, and completely independent of how (or even if) the final error 
is rendered to a console or logging backend.

> 💡 **Table of Contents:**
> * [⚙️ Architectural Concept and Role](#-architectural-concept-and-role)
> * [📋 Complete Attribute Matrix](#-complete-attribute-matrix)
> * [🔄 Stack Tracing and caller_info Mechanics](#-stack-tracing-and-caller_info-mechanics)
> * [🌐 Serialization Pipeline](#-serialization-pipeline)
> * [📖 Reference Implementation](#-reference-implementation)

---

## ⚙️ Architectural Concept and Role

* **State Isolation:** 
The class serves exclusively as a container. 
It declares data fields, enforces default values, exposes a lazily evaluated location property, 
and provides serialization methods. It contains zero printing, terminal-escaped formatting, 
or layout-drawing logic.
* **Structural Compatibility:** 
The dataclass structurally satisfies the `SimpleExceptionDataProtocol` interface. 
Every concrete error class in the `SimpleException` family either inherits directly 
from this class (via cooperative multiple inheritance) or wraps it as an internal data payload container.
* **The `UNSET` Sentinel Token:** 
To distinguish between a property that was omitted entirely during instantiation 
and a property that was intentionally passed as a literal `None`, the `value` field 
leverages a dedicated internal sentinel token named `UNSET`.

---

## 📋 Complete Attribute Matrix

The following table details every data field managed by `SimpleExceptionData`.

| Attribute               | Data Type                 | Default Value | Description                                                                                                    |
| :---------------------- | :------------------------ | :------------ | :------------------------------------------------------------------------------------------------------------- |
| `error_name`            | `str`                     | `"ERROR"`     | The primary exception category/name printed in the visual header banner.                                       |
| `exception`             | `type[Exception]`         | `None`        | Raw exception class reference to preserve structural class hierarchy checks.                                   |
| `intercepted_exception` | `str`                     | `None`        | Textual identifier snapshot representing a caught underlying exception from a `try-except` block.              |
| `value`                 | `Any`                     | `UNSET`       | The live runtime object that failed validation (handles `None` natively using the `UNSET` sentinel).          |
| `label`                 | `str`                     | `None`        | Explanatory context identifier tag for the inspected value (e.g., `"user_id"`).                               |
| `expected`              | `str`                     | `None`        | Specification constraint description detailing what state was anticipated.                                     |
| `message`               | `str`                     | `None`        | A traditional developer-facing free-text error message.                                                        |
| `problem`               | `str` / `tuple[str, ...]` | `None`        | Explanation of what failed. Supports multi-line layout formatting via tuples.                                 |
| `context`               | `str` / `tuple[str, ...]` | `None`        | Supplementary environment metadata (IP addresses, hashes, request IDs).                                       |
| `how_to_fix`            | `str` / `tuple[str, ...]` | `None`        | Actionable mitigation steps, formatted into a visual checklist.                                                |
| `get_location`          | `int` / `bool`            | `True`        | Activation flag or custom depth offset integer guiding the stack frame lookup loop.                           |
| `skip_locations`        | `tuple[str, ...]`         | `()`          | Filepath patterns or framework modules to filter out during execution traceback scanning.                     |
| `_cached_caller_info`   | `dict`                    | `UNSET`       | Low-level private cache slot backing the lazy location metadata evaluation lifecycle.                         |
| `oneline`               | `bool`                    | `False`       | Formatting hint signal directing the exception to output a single flattened row.                              |

[🔼 Back to Top](#-simpleexceptiondata)

---

## 🔄 Stack Tracing and caller_info Mechanics

Resolving the file path and line number where an error occurred (call-site tracing) 
is a computationally heavy task because it requires walking active frame objects 
inside the running Python interpreter. `SimpleExceptionData` minimizes this runtime footprint 
using a **Lazy Evaluation Pipeline** combined with **Defensive Caching**.

### 🔄 The `caller_info` Lifecycle

1. **Instantiation:** 
When an exception is raised, no traceback inspection occurs. 
The internal field `_cached_caller_info` is initialized as `UNSET`.
2. **First Access:** 
The moment a renderer or diagnostic exporter queries the `data.caller_info` property 
for the first time, the engine checks the configuration state:
   * If `get_location` is set to `False`, the property immediately returns `None` 
   without inspecting any frames.
   * If `_cached_caller_info` matches `UNSET`, the engine executes the isolated 
   stack-tracing utility `extract_caller_info()`.
3. **Caching the State:** 
The resolved frame metadata dictionary (containing `file`, `path`, `line`, and `function`) 
or `None` (if resolution failed or was filtered out) is written back to the private cache field.
4. **Subsequent Access:** 
Any future reads of the `caller_info` property bypass the stack analyzer entirely, 
pulling the cached dictionary instantly with zero performance overhead.

---

### 🔬 Inside the `extract_caller_info` Engine

The `extract_caller_info` utility is a highly optimized, decoupled diagnostic instrument 
designed around five critical design principles:

#### 1. Zero Disk I/O Overhead

When capturing the traceback stack via `inspect.stack(context=0)`, the engine strictly sets `context=0`. 
This tells the Python interpreter to skip reading surrounding source code lines from disk, 
rendering stack scanning incredibly fast.

#### 2. Cross-Platform Path Normalization

All file paths from the active stack frames and all custom exclusion patterns (`excluded_patterns`) 
are converted to POSIX paths via `Path.as_posix()` before comparison. 
This ensures absolute matching parity across Windows (which uses backslashes `\`) 
and Unix/Linux/macOS (which use forward slashes `/`).

#### 3. Content-Based Filtering over Hardcoded Offsets

Instead of relying on fragile, hardcoded integer index offsets (such as "always skip 3 frames") 
that break during library refactoring, the engine traverses the stack dynamically. 
It skips any frames matching blacklisted directories or package paths and targets 
the first meaningful frame matching the desired depth limit (`expected_frames`).

#### 4. The "Fallout" Safety Net Pattern

If a developer configures the blacklist so aggressively that every frame up to the root 
of the workspace is excluded, the engine refuses to collapse with an empty value. 
During traversal, it maintains a continuous reference to the last frame physically touched (`final_frame`). 
If the search-and-verify loop completes without meeting the `expected_frames` target, 
it gracefully returns this last-touched frame as a safety net.

#### 5. The "Do No Harm" Zero-Crash Directive

As a diagnostic utility executing during active error handling, this function must never cause a crash. 
The execution body is wrapped within a global `try-except` block. 
Any unexpected interpreter anomalies (e.g., corrupt stack frames) are caught silently, 
degrading gracefully to return `None`.

[🔼 Back to Top](#-simpleexceptiondata)

---

## 🌐 Serialization Pipeline

`SimpleExceptionData` provides built-in serializers to convert exception state 
into clean data formats suitable for log aggregators, Application Performance Monitoring 
(APM) tools (like Sentry or Datadog), or user-facing API error responses.

### 🌐 `to_dict()` – Clean Public Export

Compiles a high-level, human-focused dictionary containing only core business diagnostic data.

* **Configuration Isolation:** 
Internal configuration flags (`oneline`, `get_location`) and location-tracking metadata 
are omitted to keep public logs clean.
* **Sentinel Filtration:** 
The serializer loops through candidate fields and filters out any attributes matching 
the `UNSET` sentinel. This prevents unconfigured fields from bloating output payloads 
with cluttered `null` or placeholder values.

### 🐞 `to_debug_dict()` – Developer Diagnostic Snapshot

Assembles a low-level snapshot dictionary intended for telemetry systems, crash logs, and debugging pipelines.

* Inherits the base structure from `to_dict()`.
* **Traceback Injection:** 
Injects the fully resolved call-site metadata under the `"caller_info"` key.
* **Interception Injection:** 
Injects the original caught exception class name (`"intercepted_exception"`).
* **Rendered Visual Capture:** 
Defensively reads (using `getattr` to protect against execution before message compilation completes) 
* and embeds the exact visual console text layout shown to the user (`"rendered_message"`).

### 📄 `to_json()` – Flat JSON Serialization

Converts the public dictionary output of `to_dict()` into a compact, un-indented JSON string representation. 
Non-primitive Python objects nested inside the exception state are safely stringified via `default=str`.

[🔼 Back to Top](#-simpleexceptiondata)

---

## 📖 Reference Implementation

Use the following complete reference implementation of the state dataclass, traceback scanner, 
and serialization functions to guide development or extend the framework.

### `SimpleExceptionData` (Dataclass)

```python
@dataclass
class SimpleExceptionData:
    """Pure state data class defining the attributes, boundaries, and defaults of SimpleException."""

    # --- Core exception info ---
    error_name: str = "ERROR"
    exception: type[Exception] | None = None
    intercepted_exception: str | None = None

    # --- Info about the inspected value ---
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

    # --- Layout Overrides ---
    oneline: bool = False

    @property
    def caller_info(self) -> dict[str, Any] | None:
        """Lazily-computed and cached filesystem call site metadata footprint."""
        if not self.get_location:
            return None

        if self._cached_caller_info is UNSET:
            self._cached_caller_info = extract_caller_info(
                expected_frames=int(self.get_location),
                excluded_patterns=self.skip_locations,
            )

        return self._cached_caller_info

    def to_dict(self: "SimpleExceptionDataProtocol") -> dict[str, Any]:
        """Serializes core public exception attributes into a clean dictionary."""
        return _to_dict(self)

    def to_debug_dict(self: "SimpleExceptionDataProtocol") -> dict[str, Any]:
        """Compiles a comprehensive diagnostic snapshot dictionary."""
        return _to_debug_dict(self)

    def to_json(self: "SimpleExceptionDataProtocol") -> str:
        """Serializes core instance public data fields into an un-indented JSON string."""
        return json.dumps(self.to_dict(), default=str)
```

### `extract_caller_info` (Traceback Utility)

```python
def extract_caller_info(
    expected_frames: int = 1,
    excluded_patterns: tuple[str, ...] = (),
) -> dict[str, Any] | None:
    """Walks the call stack and returns info about the requested relevant frame."""
    try:
        stack = inspect.stack(context=0)
        if not stack:
            return None

        excluded = set()
        if excluded_patterns:
            excluded.update(Path(p).as_posix() for p in excluded_patterns)

        final_frame = None
        valid_count = 0

        for frame in stack[1:]:
            final_frame = frame
            normalized_path = Path(frame.filename).as_posix()

            if not any(p in normalized_path for p in excluded):
                valid_count += 1
                if valid_count == expected_frames:
                    break

        if final_frame:
            return {
                "file": os.path.basename(final_frame.filename),
                "path": final_frame.filename,
                "line": final_frame.lineno,
                "function": final_frame.function,
            }

        return None

    except Exception:
        return None
```

### Serialization Utilities (`to_dict` & `to_debug_dict`)

```python
def to_dict(
    self: "SimpleExceptionDataProtocol"
) -> dict[str, Any]:
    """Serializes core public exception attributes into a clean dictionary."""
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

    return {key: val for key, val in candidates.items() if val is not UNSET}
```

```python
def to_debug_dict(
    self: "SimpleExceptionDataProtocol"
) -> dict[str, Any]:
    """Compiles a comprehensive diagnostic snapshot dictionary for developers."""
    result = to_dict(self)

    if self.caller_info:
        result["caller_info"] = self.caller_info

    if self.intercepted_exception:
        result["intercepted_exception"] = self.intercepted_exception

    rendered_msg = getattr(self, "rendered_message", None)
    if rendered_msg:
        result["rendered_message"] = rendered_msg

    return result
```

[🔼 Back to Top](#-simpleexceptiondata)

---

[⬅️ Back to README](../README.md)