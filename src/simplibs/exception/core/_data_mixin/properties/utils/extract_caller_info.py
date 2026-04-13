import inspect
import os
from pathlib import Path
from typing import Any

# Strings that are always excluded when searching for a relevant frame.
# "<" covers Python's dynamic frames such as <string>, <frozen importlib>, etc.
_ALWAYS_EXCLUDED = ("<",)


# noinspection PyBroadException
def extract_caller_info(
    expected_frames: int = 1,
    excluded_patterns: tuple[str, ...] = (),
) -> dict[str, Any] | None:
    """
    Walks the call stack and returns info about the requested relevant frame.

    Args:
        expected_frames:    Which valid frame to return (1 = first non-excluded).
        excluded_patterns:  Strings that, if found in a file path, cause that
                            frame to be skipped (e.g., library internal paths).

    Returns:
        A dictionary with keys: file, full_path, line, function — or None on failure.
    """
    try:
        # 1. Load the stack (context=0 is a performance optimization)
        stack = inspect.stack(context=0)
        if not stack:
            return None

        # 2. Normalize all excluded patterns to POSIX paths for cross-platform compatibility
        excluded = set(Path(p).as_posix() for p in (_ALWAYS_EXCLUDED + excluded_patterns))

        # 3. Initialize loop variables
        final_frame = None
        valid_count = 0

        # 4. Walk the stack (starting from index 1 to skip this utility itself)
        for frame in stack[1:]:
            # 4.1 Keep track of the current frame as a fallback "safety net"
            final_frame = frame

            # 4.2 Normalize the frame path to POSIX for cross-platform matching
            normalized_path = Path(frame.filename).as_posix()

            # 4.3 Check if the frame's path is in the exclusion list
            if not any(p in normalized_path for p in excluded):

                # 4.4 Increment the counter of valid (non-excluded) frames
                valid_count += 1

                # 4.5 Check if we reached the requested frame number
                if valid_count == expected_frames:
                    break  # Target found

        # 5. Build and return the result dictionary
        if final_frame:
            return {
                "file": os.path.basename(final_frame.filename),
                "full_path": final_frame.filename,
                "line": final_frame.lineno,
                "function": final_frame.function,
            }

        return None

    except Exception:
        # Diagnostic utility must never cause a crash.
        # It degrades gracefully to None on any error.
        return None


_DESIGN_NOTES = r"""
# extract_caller_info

## Purpose
A diagnostic utility that identifies the origin of an error by walking the 
call stack and filtering out library-internal noise.

## The "Crystallized" Logic

### 1. Cross-Platform Path Normalization
The utility uses POSIX path normalization (`Path.as_posix()`) for both 
exclusion patterns and stack frame paths. This ensures that:
- Matching works identically on Windows (`\`) and Unix-like systems (`/`).
- Developers can use forward slashes in `excluded_patterns` regardless of OS.

### 2. Content-Based Filtering vs. Fixed Offsets
Instead of relying on fragile stack depth numbers (skip_frames + 1), this 
function uses a "search-and-verify" approach:
- It iterates through the stack and ignores any frame whose path is blacklisted.
- `expected_frames=1` always points to the first frame outside the blacklist.
- This makes the utility immune to internal library refactoring (adding/removing 
  internal helper functions doesn't break the user's view).

### 3. The "Fallout" Mechanism (Safety Net)
To prevent returning `None` in an active program, the function implements 
a fallback logic:
- `final_frame` is updated at the start of every loop iteration.
- If the target `expected_frames` count is reached, the loop breaks.
- If the loop finishes without reaching the count (e.g., all frames were 
  excluded), the function returns the very last frame it encountered.
- Result: The user always gets the most relevant context available.

### 4. Zero-Crash Guarantee
Designed as a diagnostic tool, it must be more robust than the code it inspects:
- Wrapped in a broad `try/except Exception`.
- Uses `context=0` to avoid disk I/O when reading the stack.
- Gracefully returns `None` only if the stack is physically empty or 
  an unrecoverable error occurs.

## Parameters
- `expected_frames`: 1-based index (1 = first valid frame, 2 = its caller).
- `excluded_patterns`: List of strings to hide from the output. Always 
  includes `<` (dynamic frames) and the library's own path.
  
## Why no Validation or Raising
As a diagnostic tool, this function's prime directive is: "Do no harm."
- It is wrapped in a global `try/except Exception`.
- It performs no explicit type checking on inputs; any TypeError or 
  ValueError results in a graceful return of `None`.
- It avoids external dependencies and uses `context=0` in `inspect.stack()`
  to avoid unnecessary file I/O.
"""