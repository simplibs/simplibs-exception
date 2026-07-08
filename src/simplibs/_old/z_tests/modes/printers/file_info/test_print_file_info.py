def print_file_info(
    caller_info: dict | None,
    *,
    prefix: str = "File info: ",
    _log_mode: bool = False
) -> str | None:
    """
    Renders standard file metadata including filename, line number, and function name.
    Safely skips internal dynamic execution frames.
    """
    if not caller_info:
        return None

    file = caller_info["file"]

    # If it is a dynamic or internal Python evaluation frame, skip the line entirely
    if file.startswith("<"):
        return None

    line = caller_info["line"]
    function = caller_info["function"]

    # 1. LOG MODE: Structured, space-separated attributes for logging frameworks
    if _log_mode:
        return f"file={file!r} line={line} function={function!r}"

    # 2. STANDARD MODE: Clean, human-readable layout separated by vertical pipes
    return f"{prefix}{file} | line: {line} | function: {function}"


_DESIGN_NOTES = """
# print_file_info

## Purpose
Renders essential location metadata (filename, line number, and function name) 
stating exactly where the error materialized, acting as the primary navigation 
anchor for debugging.

## Dynamic Frame Filtering
Consistent with `print_file_path`, this function short-circuits if the `file` 
attribute begins with `<` (e.g., `<string>`). This ensures we don't dump meaningless, 
non-existent file metadata into the output when code runs inside dynamic execution 
environments like `exec()` or interactive REPL shells.

## Log Mode Structural Integrity
When `_log_mode=True`, the function generates an explicit key-value string:
`file='utils.py' line=42 function='parse_data'`. 
Both `file` and `function` are processed with the `!r` flag. Since filenames can 
contain spaces and Python functions can have diverse naming patterns or wrappers, 
wrapping them in native representation quotes keeps log aggregators happy and prevents 
unexpected row splitting. The `line` property is a guaranteed integer, so it is 
emitted safely without quotes.

## Usage
Used hand-in-hand with the full path printer to provide a comprehensive location footprint:
```python
lines = [
    # ...
    print_file_info(location),
    print_file_path(location),
    # ...
]
"""

