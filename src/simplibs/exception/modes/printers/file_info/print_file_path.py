def print_file_path(
    caller_info: dict | None,
    *,
    prefix: str = "File path: ",
    _log_mode: bool = False
) -> str | None:
    """
    Renders the absolute or full filesystem path of the file where the exception was raised.

    If the input value is empty or omitted, the function gracefully returns None.

    Output Formats:
        Standard Mode:
            Structure: <PREFIX><PATH>
            Example:   File path: /home/user/project/src/auth/service.py

        Log Mode (_log_mode=True):
            Structure: path='<PATH>'
            Example:   path='/home/user/project/src/auth/service.py'
    """
    if not caller_info:
        return None

    path = caller_info["path"]

    # 1. LOG MODE: Secure string representation handling directory slashes
    if _log_mode:
        return f"path={path!r}"

    # 2. STANDARD MODE: Human-friendly literal file path rendering
    return prefix + path


_DESIGN_NOTES = """
# print_file_path

## Purpose
Renders the complete filesystem path pointing to the source file where the exception 
was generated, enabling developers to jump directly to the root cause.

## Data Lifecycle & Frame Trust
This function operates under the architectural assumption that the incoming 
`caller_info` dictionary originates exclusively from the standard `SimpleException` 
processing pipeline. 

During that lifecycle, `process_skip_locations` forcefully merges any user-defined 
`LOCATION_BLACKLIST` or `skip_locations` parameters with `SimpleExceptionSettings._SYSTEM_BLACKLIST`. 
Because `_SYSTEM_BLACKLIST` permanently contains `"<"` and `"simplibs/exception"`, all internal 
Python evaluation paths (such as `<string>`) and internal framework internals are guaranteed 
to be stripped out *before* reaching this formatting layer. 

As a result, this printer contains no defensive filtering or validation logic for 
dynamic paths, maintaining a zero-redundancy, high-performance rendering path.

## Cross-Platform Log Safety via Repr (!r)
When `_log_mode=True`, the absolute file path is encoded using the `!r` formatting flag. 
Filesystem paths are inherently volatile across environments—Windows paths utilize 
backslashes (`\\`) and paths on any OS may contain spaces or localized characters. 
Using `!r` ensures that slashes are properly escaped and the entire path string 
is cleanly quoted, preventing issues with downstream log parsers.

## Usage
Positioned within the metadata phase of the layout generation chain:
```python
lines = [
    # ...
    print_file_info(location),
    print_file_path(location),
    # ...
]
"""