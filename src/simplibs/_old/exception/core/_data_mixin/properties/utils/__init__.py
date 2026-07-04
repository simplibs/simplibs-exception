from .extract_caller_info import extract_caller_info


_DESIGN_NOTES = """



| Name                  | Description                                                   |
|-----------------------|---------------------------------------------------------------|
| `extract_caller_info` | Diagnostic function for determining the call site in the stack |

## Notes
- `extract_caller_info` is independent of the rest of the library —
  it has no dependencies and can be used anywhere.
"""