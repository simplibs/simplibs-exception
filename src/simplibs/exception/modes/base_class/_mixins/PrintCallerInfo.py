# noinspection PyMethodMayBeStatic
class PrintCallerInfoMixin:
    """Mixin providing formatting of exception call site information."""

    def _print_caller_info(self, caller_info: dict | None, as_dict: bool = False) -> str | dict:
        """
        Formats the provided call site information as a string or dictionary.

        Args:
            caller_info: Dictionary with keys file, full_path, line, function —
                         or None if the location was not found or is disabled.
            as_dict:     If True, returns raw data as a dictionary (suited for LOG mode).

        Returns:
            When as_dict=False: 'File: ... | Line: ... | Path: ... | Function: ...'
            When as_dict=True:  {'file': '...', 'line': ..., 'path': '...', 'func': '...'}
        """
        # Safe handling of missing data — caller_info is None when
        # get_location=False or when extract_caller_info found no relevant frame
        if not caller_info:
            if as_dict:
                return {"file": "unknown", "line": 0, "path": "unknown", "func": "unknown"}
            return "Location: Unknown"

        # Variant for machine processing (LOG mode)
        if as_dict:
            return {
                "file": caller_info.get("file", "unknown"),
                "line": caller_info.get("line", 0),
                "path": caller_info.get("full_path", "unknown"),
                "func": caller_info.get("function", "unknown"),
            }

        # Variant for human reading (PRETTY, SIMPLE, ONELINE modes)
        return " | ".join((
            f"File: {caller_info['file']}",
            f"Line: {caller_info['line']}",
            f"Path: {caller_info['full_path']}",
            f"Function: {caller_info['function']}",
        ))


_DESIGN_NOTES = """
# PrintCallerInfoMixin

## Purpose
Formats pre-computed call site information (file, line, path, function)
into an output string or dictionary.

The mixin deliberately performs no computation or stack introspection —
it receives ready-made data as a parameter. Location resolution happens
exclusively in `render_message` inside `ModeBase`, where the call stack
is at a predictable depth. Separating computation from formatting ensures
that `skip_frames` is always correct regardless of which output method
calls `_print_caller_info`.

## The caller_info parameter
A dictionary with keys `file`, `full_path`, `line`, `function` — the output
of `extract_caller_info`. The value is `None` in two cases:
- `_get_location` is `False` or `0` — location reporting is intentionally disabled
- `extract_caller_info` found no relevant frame or raised an exception

In both cases the method returns a safe fallback instead of raising a `TypeError`.

## The as_dict parameter
Added to support LOG mode, which uses a `key=value` format.
- `False` (default) — a formatted string for human reading
- `True` — a raw dictionary that LOG mode assembles into its own format

Without this parameter, LOG mode would have to parse the formatted string
back into its parts — which would be fragile and unnecessary.

## Output (as_dict=False)
    File: filename.py | Line: 42 | Path: /full/path.py | Function: my_function

## Output (as_dict=True)
    {"file": "filename.py", "line": 42, "path": "/full/path.py", "func": "my_function"}

## Notes
- This method never raises an exception — missing or invalid caller_info
  is handled with a safe fallback.
- Marked `# noinspection PyMethodMayBeStatic` — as a mixin method it must
  take this form to be accessible via `self` in subclasses of `ModeBase`.
"""