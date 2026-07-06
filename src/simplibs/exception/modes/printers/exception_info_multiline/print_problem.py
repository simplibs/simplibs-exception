# Outers
from ..dividers import EMPTY_PREFIX


def print_problem(
    problem: tuple[str, ...] | str | None,
    *,
    prefix: str = "Problem:   ",
    _log_mode: bool = False,
    _oneline: bool = False,
) -> str | None:
    """
    Renders the exception's problem statement supporting standard multi-line, flat oneline, or logfmt formatting.

    If the input value is empty or omitted, the function gracefully returns None.

    Output Formats:
        Standard Mode (Multi-line layout):
            Structure: <PREFIX><PROBLEM_LINE_1><EMPTY_PREFIX><PROBLEM_LINE_2>...
            Example:   Problem:   The database connection timed out after 5 seconds.
                                  Please check your network configuration and try again.

        Oneline Mode (_oneline=True):
            Structure: <PREFIX><PROBLEM_LINE_1> <PROBLEM_LINE_2>...
            Example:   Problem:   The database connection timed out after 5 seconds. Please check your network configuration and try again.

        Log Mode (_log_mode=True):
            Structure: problem='<PROBLEM_FLATTENED_WITH_SPACES>'
            Example:   problem='The database connection timed out after 5 seconds. Please check your network configuration and try again.'
    """
    if not problem:
        return None

    # --- FAST PATH: Optimize for primitive flat string inputs ---
    if isinstance(problem, str):
        if _log_mode:
            return f"problem={problem!r}"
        return prefix + problem

    # --- STANDARD PATH: Process multi-line collections (tuple) ---
    # 1. LOG MODE: Flatten all lines into a single string for machine processing
    if _log_mode:
        flat_problem = " ".join(problem)
        return f"problem={flat_problem!r}"

    # 2. ONELINE MODE: Inline all items separated by spaces, ignoring vertical margins
    if _oneline:
        return prefix + " ".join(problem)

    # 3. STANDARD MODE: Inline first item, align subsequent items via EMPTY_PREFIX
    first_line = problem[0]
    remaining_lines = problem[1:]

    if not remaining_lines:
        return prefix + first_line

    return prefix + first_line + EMPTY_PREFIX + EMPTY_PREFIX.join(remaining_lines)


_DESIGN_NOTES = """
# print_problem

## Purpose
Formats the `problem` data field (a hybrid single string or a collection of strings) into a 
visually aligned text block, flattens it into a horizontal string for dense terminal streams, 
or pairs it down to a single token for machine log file emission.

## Architectural Optimization: Fast-Path vs. Standard Path

To maximize execution efficiency, the function dynamically forks its internal evaluation logic 
based on the underlying data type:

### 1. Primitive String Fast-Path (`isinstance(problem, str)`)
If the normalization layer delivers a single primitive string, the engine completely bypasses tuple 
slicing, array loops, and iterator joins. It fires an ultra-fast string concatenation directly. 
This yields a massive performance boost for the most common use-cases.

### 2. Multi-Line Collection Path (`isinstance(problem, tuple)`)
If multiple lines are detected, the function processes the data through the standard structural matrix:
- **Standard Mode (The Inline-First Pattern)**: The first line binds to the header `prefix`. 
  Subsequent items are glued together via `EMPTY_PREFIX` (a newline `\\n` combined with layout spaces), 
  forming a perfect vertical aligned column block.
- **Oneline Mode (`_oneline=True`)**: Drops all alignment indentation padding and collapses all 
  tuple text entries into a flat space-separated row, preserving the human prefix tag.
- **Log Mode (`_log_mode=True`)**: Discards the human prefix, joins lines with spaces, and wraps the 
  entire outcome inside safe `repr()` quotes using the `!r` formatting token to safeguard machine parsers.

## Visual Output Typology

```text
# Standard Path (Multi-line layout)
Problem:   This is the first line of the problem statement.
           This is the second line, perfectly aligned.

# Fast-Path / Oneline Mode (Flat row layout)
Problem: This is the first line of the problem statement. This is the second line.

# Log Mode (Machine-readable layout)
problem='This is the first line of the problem statement. This is the second line.'

```

## Usage Matrix

```python
# Multi-line collection or single string human view
print_problem(data.problem)

# Flat horizontal terminal row layout
print_problem(data.problem, _oneline=True)

# Machine-readable telemetry log stream token
print_problem(data.problem, _log_mode=True)

```

"""