def print_file_path(
    caller_info: dict | None,
    *,
    prefix: str = "File path: ",
    _log_mode: bool = False
) -> str | None:
    """
    Renders the absolute or full filesystem path of the file where the exception was raised.
    Safely skips internal dynamic execution frames.
    """
    if not caller_info:
        return None

    path = caller_info["path"]

    # If it is a dynamic or internal Python evaluation frame, skip the line entirely
    if path.startswith("<"):
        return None

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

## Dynamic Frame Filtering
The function inspects the `path` and short-circuits returning `None` if it starts 
with a `<` token (e.g., `<string>`, `<stdin>`, `<module>`). These patterns appear 
when code is executed dynamically via `eval()`, `exec()`, or interactive REPL 
sessions. Because these paths do not point to real, physical files on the disk, 
rendering them would confuse the user and clutter the layout.

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