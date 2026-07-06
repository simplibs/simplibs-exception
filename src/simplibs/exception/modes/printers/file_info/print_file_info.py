def print_file_info(
    caller_info: dict | None,
    *,
    prefix: str = "File info: ",
    _log_mode: bool = False
) -> str | None:
    """
    Renders standard file metadata including filename, line number, and function name.

    If the input value is empty or omitted, the function gracefully returns None.

    Output Formats:
        Standard Mode:
            Structure: <PREFIX><FILE> | line: <LINE> | function: <FUNCTION>
            Example:   File info: src/auth/service.py | line: 42 | function: login_user

        Log Mode (_log_mode=True):
            Structure: file='<FILE>' line=<LINE> function='<FUNCTION>'
            Example:   file='src/auth/service.py' line=42 function='login_user'
    """
    if not caller_info:
        return None

    file = caller_info["file"]
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

## Data Lifecycle & Frame Trust
This function operates under the architectural assumption that the incoming 
`caller_info` dictionary originates exclusively from the standard `SimpleException` 
processing pipeline. 

During that lifecycle, `process_skip_locations` forcefully merges any user-defined 
`LOCATION_BLACKLIST` or `skip_locations` parameters with `SimpleExceptionSettings._SYSTEM_BLACKLIST`. 
Because `_SYSTEM_BLACKLIST` permanently contains `"<"` and `"simplibs/exception"`, all internal 
Python evaluation frames (such as `<string>`) and internal framework internals are guaranteed 
to be stripped out *before* reaching this formatting layer. 

As a result, this printer contains no defensive filtering or validation logic for 
dynamic frames, maintaining a zero-redundancy, high-performance rendering path.

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

