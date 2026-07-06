# Outers
from ..dividers import DOT_PREFIX


def print_how_to_fix(
    how_to_fix: tuple[str, ...] | str | None,
    *,
    prefix: str = "🔧 How to fix:",
    _log_mode: bool = False,
    _oneline: bool = False,
) -> str | None:
    """
    Renders actionable mitigation steps supporting standard multi-line checklists, flat oneline, or logfmt formatting.

    If the input value is empty or omitted, the function gracefully returns None.

    Output Formats:
        Standard Mode (Rich vertical checklist layout):
            Structure: <PREFIX><DOT_PREFIX><STEP_1><DOT_PREFIX><STEP_2>...
            Example:   🔧 How to fix:
                            • Ensure the input field enforces front-end email format filtering.
                            • Check the downstream gateway router payload parser encoding schema.

        Oneline Mode (_oneline=True):
            Structure: <PREFIX> <STEP_1> <STEP_2>...
            Example:   🔧 How to fix: Ensure the input field enforces front-end email format filtering. Check the downstream gateway router payload parser encoding schema.

        Log Mode (_log_mode=True):
            Structure: how_to_fix='<STEPS_FLATTENED_WITH_SPACES>'
            Example:   how_to_fix='Ensure the input field enforces front-end email format filtering. Check the downstream gateway router payload parser encoding schema.'
    """
    if not how_to_fix:
        return None

    # --- FAST PATH: Optimize for primitive flat string inputs ---
    if isinstance(how_to_fix, str):
        if _log_mode:
            return f"how_to_fix={how_to_fix!r}"
        if _oneline:
            return prefix + " " + how_to_fix
        return prefix + DOT_PREFIX + how_to_fix

    # --- STANDARD PATH: Process multi-line collections (tuple) ---
    # 1. LOG MODE: Flatten all checklist steps into a single machine-safe token
    if _log_mode:
        flat_fix = " ".join(how_to_fix)
        return f"how_to_fix={flat_fix!r}"

    # 2. ONELINE MODE: Inline all items separated by spaces, removing vertical bullets
    if _oneline:
        return prefix + " " + " ".join(how_to_fix)

    # 3. STANDARD MODE: Rich vertical bulleted list layout
    return prefix + DOT_PREFIX + DOT_PREFIX.join(how_to_fix)


_DESIGN_NOTES = """
# print_how_to_fix

## Purpose
Formats a hybrid single string or a collection of human-readable mitigation steps (`how_to_fix`) 
into a highly structured vertical checklist block, a horizontal terminal row segment, or a 
machine-safe logfmt token.

## Universal API Symmetry & Execution Layouts

To enforce absolute predictable design patterns across the entire printer suite, this function 
fully supports all execution control flags, ensuring it never returns `None` when data is present:

### 1. Primitive String Fast-Path (`isinstance(how_to_fix, str)`)
If the input contains only a single mitigation line, the engine bypasses collection loops and 
directly evaluates the output based on active flags, providing ultra-fast execution.

### 2. Standard Multi-Line View (The Bullet-Column Pattern)
When rendering a full collection for humans in a standard layout, the engine uses explicit string 
concatenation to append a bullet signature (`DOT_PREFIX`) before *every* item:
```python
return prefix + DOT_PREFIX + DOT_PREFIX.join(how_to_fix)

```

Because Python's native `str.join()` only inserts delimiters *between* collection elements,
pre-injecting `DOT_PREFIX` immediately after the header `prefix` guarantees that every single item,
including the very first row, is visually aligned and preceded by the identical vertical bullet layout.

### 3. Oneline Mode (`_oneline=True`)

Designed for horizontal row streaming. It completely suppresses the vertical newline bullet tokens
(`DOT_PREFIX`) and merges all mitigation steps into a flat, space-separated sequence while
preserving the human-friendly prefix header:

```text
🔧 How to fix: Step one instructions. Step two instructions.

```

### 4. Log Mode (`_log_mode=True`)

Optimized for production row-based machine log parsers (Logstash, Datadog). It discards the human
prefix and structural bullets, joins all steps with a standard space, and seals the output inside
safe `repr()` quotes via the `!r` formatting token to keep the log stream corruption-free:

```text
how_to_fix='Step one instructions. Step two instructions.'

```

## Visual Output Typology

```text
# Standard Mode (Multi-line layout)
🔧 How to fix:
   • This is the first actionable step item.
   • This is the second actionable step item.

# Oneline Mode (Flat terminal row layout)
🔧 How to fix: This is the first actionable step item. This is the second actionable step item.

# Log Mode (Machine-readable layout)
how_to_fix='This is the first actionable step item. This is the second actionable step item.'

```

## Usage Matrix

```python
# Multi-line human view (Skipped in native ONELINE/LOG modes via layout managers)
print_how_to_fix(data.how_to_fix)

# Flat horizontal terminal row layout
print_how_to_fix(data.how_to_fix, _oneline=True)

# Machine-readable telemetry log stream token
print_how_to_fix(data.how_to_fix, _log_mode=True)

```

"""