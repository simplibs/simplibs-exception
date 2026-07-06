DOUBLE_LINE = "═" * 65


_DESIGN_NOTES = """
# DOUBLE_LINE

## Purpose
Acts as the primary structural framing boundary for rich exception layouts (such as `PrettyMessage`).

## Design Role
- Used at the absolute top and bottom of the exception layout to close the visual box.
- Used as a strong separator immediately after the error identity header (`print_intro`).
"""