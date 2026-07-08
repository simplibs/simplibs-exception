EMPTY_PREFIX = "\n           "


_DESIGN_NOTES = """
# EMPTY_PREFIX

## Purpose
Provides vertical multi-line alignment for content-heavy fields using the "inline-first" pattern.

## Design Role
- Contains a newline followed by exactly 11 spaces.
- This length matches the fixed width of standard labels like `Problem:   ` and `Context:   `.
- Ensures that subsequent lines of a multi-line string form a perfectly straight vertical column, keeping the layout sharp and readable.
"""