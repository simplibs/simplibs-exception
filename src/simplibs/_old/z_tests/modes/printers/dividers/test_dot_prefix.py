DOT_PREFIX = "\n     • "


_DESIGN_NOTES = """
# DOT_PREFIX

## Purpose
Provides a bulleted list layout exclusively for the actionable mitigation block.

## Design Role
- Contains a newline followed by 5 padding spaces and a bullet character (`•`).
- Unlike `EMPTY_PREFIX`, it does not align perfectly with the 11-character left margin. Instead, it creates a deliberate, slight indent under the `🔧 How to fix:` header.
- This creates a clear visual hierarchy, grouping all troubleshooting steps into an obvious, distinct checklist.
"""