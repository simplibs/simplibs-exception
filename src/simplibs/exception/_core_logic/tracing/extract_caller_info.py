import inspect
import os
from pathlib import Path
from typing import Any


# noinspection PyBroadException
def extract_caller_info(
    expected_frames: int = 1,
    excluded_patterns: tuple[str, ...] = (),
) -> dict[str, Any] | None:
    """Walks the call stack and returns info about the requested relevant frame.

    Args:
        expected_frames:    Which valid frame to return (1 = first non-excluded).
        excluded_patterns:  Fully compiled tuple of strings that, if found in a
                            file path, cause that frame to be skipped.

    Returns:
        A dictionary with keys: file, path, line, function — or None on failure.
    """
    try:
        # 1. Load the stack (context=0 is a strict performance optimization avoiding disk I/O)
        stack = inspect.stack(context=0)
        if not stack:
            return None

        # 2. Normalize all excluded patterns to POSIX paths. Safely handles any iterable sequence.
        excluded = set()
        if excluded_patterns:
            excluded.update(Path(p).as_posix() for p in excluded_patterns)

        # 3. Initialize loop variables
        final_frame = None
        valid_count = 0

        # 4. Walk the stack (starting from index 1 to skip this utility frame itself)
        for frame in stack[1:]:
            # 4.1 Keep track of the current frame as a fallback "safety net"
            final_frame = frame

            # 4.2 Normalize the frame path to POSIX for cross-platform matching
            normalized_path = Path(frame.filename).as_posix()

            # 4.3 Check if the frame's path contains any blacklisted patterns
            if not any(p in normalized_path for p in excluded):
                # 4.4 Increment the counter of valid (non-excluded) frames
                valid_count += 1

                # 4.5 Check if we reached the requested frame number
                if valid_count == expected_frames:
                    break  # Target found

        # 5. Build and return the result dictionary from the chosen frame context
        if final_frame:
            return {
                "file": os.path.basename(final_frame.filename),
                "path": final_frame.filename,
                "line": final_frame.lineno,
                "function": final_frame.function,
            }

        return None

    except Exception:
        # Diagnostic utility must never cause a crash.
        # It degrades gracefully to None on any error.
        # Implements the absolute "Do no harm" architectural directive.
        return None


_DESIGN_NOTES = r"""
# extract_caller_info

## Purpose
A diagnostic utility that identifies the origin of an error by walking the active Python 
call stack and extracting metadata from the most relevant, non-excluded frame.

## Decoupled Architectural Design
This engine operates in a state of absolute decoupling. It contains no hardcoded references to 
core interpreter virtual symbols (`"<"`) or framework-specific internal directory layouts (`"simplibs/exception"`). 
Instead, it consumes a single pre-compiled source of truth through the `excluded_patterns` argument. 
The compilation and prioritization of these patterns are fully delegated upstream to the exception 
initialization lifecycle handlers.

## Core Pillars of the Crystallized Logic

### 1. Cross-Platform Path Normalization
The utility converts all search vectors and target frames into explicit POSIX path strings (`Path.as_posix()`). 
This enforces absolute cross-platform parity:
- Evaluation mirrors perfectly between Windows backslashes (`\`) and Unix forward slashes (`/`).
- Upstream processors can pass exclusion patterns using standard forward slashes, independent of the hosting OS.

### 2. Content-Based Filtering vs. Fixed Offsets
Instead of relying on fragile hardcoded stack depth numbers (such as `skip_frames + 1`), which break 
whenever internal modules are refactored, the scanner utilizes an active "search-and-verify" loop. 
It filters out blacklisted structures dynamically, meaning `expected_frames=1` reliably targets the first 
meaningful frame outside the provided exclusion grid, ensuring high code-change resilience.

### 3. The "Fallout" Mechanism (Safety Net Pattern)
To eliminate the risk of returning `None` in a perfectly operational runtime environment, the engine 
implements a strict fallback strategy. `final_frame` updates immediately upon every loop pass. If the 
loop ends without meeting the targeted `expected_frames` count (e.g., if the user blacklisted their entire 
workspace), the utility refuses to fail blindly; instead, it falls back and returns the very last frame 
it physically touched. 

### 4. Zero-Crash Guarantee Directive
As a diagnostic instrument inspecting ongoing failures, this utility operates under a strict "Do no harm" 
mandate. It wraps execution inside a global `try/except Exception` block and sets `context=0` inside 
`inspect.stack()` to prevent unnecessary synchronous disk read I/O operations. Any unexpected parameter type 
anomalies trigger a silent, graceful return of `None`.
"""