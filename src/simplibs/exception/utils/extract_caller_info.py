import inspect
import os
from typing import Any


# Strings that are always excluded when searching for a relevant frame.
# "<" covers Python's dynamic frames such as <string>, <frozen importlib>, etc.
_ALWAYS_EXCLUDED = ("<",)

# noinspection PyBroadException
def extract_caller_info(
    skip_frames: int = 1,
    excluded_patterns: tuple[str, ...] = (),
) -> dict[str, Any] | None:
    """
    Walks the call stack and returns info about the first relevant frame.

    Args:
        skip_frames:        Number of frames to skip from the call site.
        excluded_patterns:  Strings that, if found anywhere in a file path,
                            cause that frame to be skipped (e.g. "simple_exception").

    Returns:
        A dictionary with keys file, full_path, line, function — or None on failure.
    """

    try:

        # 1. Load the stack and initialise variables
        stack = inspect.stack(context=0)
        excluded = set(_ALWAYS_EXCLUDED + excluded_patterns)
        start_index = skip_frames + 1

        # 2. Walk the stack and find the first matching frame
        for frame_info in stack[start_index:]:

            # 2.1 Skip if the file path contains any of the excluded strings
            if any(p in frame_info.filename for p in excluded):
                continue

            # 2.2 On a match, build and return the result
            return {
                "file":      os.path.basename(frame_info.filename),
                "full_path": frame_info.filename,
                "line":      frame_info.lineno,
                "function":  frame_info.function,
            }

        # 3. No relevant frame found — return None
        return None

    # If the process raises an exception, return None
    except Exception:
        return None


_DESIGN_NOTES = """
# extract_caller_info

## Purpose
A diagnostic utility function — determines where in the codebase execution
originated by walking the call stack and returning info about the first
relevant frame.

## Output dictionary
```python
{
    "file":      "filename.py",        # basename without path
    "full_path": "/full/path.py",      # absolute path
    "line":      42,                   # line number (int)
    "function":  "function_name",      # function name or "<module>"
}
```

## How skip_frames works
The internal `+1` always skips `extract_caller_info` itself.
`skip_frames` then skips additional layers of the stack above it:
```
0  extract_caller_info   ← always skipped (+1)
1  direct caller         ← skip_frames=0
2  caller's caller       ← skip_frames=1 (default)
```

## How excluded_patterns works
Each string in `excluded_patterns` is searched for anywhere in the file path —
if found, the frame is skipped. This makes it easy to exclude entire parts
of a project with a single entry:
```python
excluded_patterns = ("simple_exception",)
# skips any frame whose path contains "simple_exception"
```

Internally, `excluded_patterns` is merged with `_ALWAYS_EXCLUDED` — a
module-level constant that always skips Python's dynamic frames
(`<string>`, `<frozen importlib>`, etc.) whose paths start with `<`.
The caller does not need to handle these technical frames manually.

## Why there is no input validation
This function is a **diagnostic utility** — its core rule is:
*it must never be the cause of a program crash.*

It would be paradoxical for a function designed for diagnostics to raise
errors itself. For this reason there is no explicit validation —
`try/except Exception` catches everything, including badly typed arguments,
and the function degrades gracefully to `None`.
```python
extract_caller_info(skip_frames="hello")
# → "hello" + 1 → TypeError → caught → returns None
```

## Why there is no fallback parameter
Fallback handling is the caller's responsibility, not the function's.
`None` as a return value on failure is sufficient — the caller can act on it:
```python
result = extract_caller_info(...) or MY_FALLBACK
```

## Why there is no silence or validate parameter
- `silence` would imply the function can raise — which contradicts its nature.
- `validate` would mean intentionally throwing exceptions — same problem.
- Anyone unsure about their inputs should validate them before calling,
  not through the function itself.

## Notes
- Python's dynamic frames (paths containing `<`) are always skipped.
- `context=0` in `inspect.stack()` is a performance optimisation — it does
  not load source code.
- This function has no dependencies on any library — it can be used anywhere.
- The `line` value in the output dictionary is an `int`; all other values are `str`.
"""