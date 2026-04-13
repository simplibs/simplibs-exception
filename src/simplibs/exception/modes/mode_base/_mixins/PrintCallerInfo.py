from typing import Any
# Outers
from ....core import SimpleExceptionData


# noinspection PyMethodMayBeStatic
class PrintCallerInfoMixin:
    """Mixin providing formatting of exception call site information from data."""

    def _print_caller_info(
        self,
        data: SimpleExceptionData,
        *,
        as_dict: bool = False
    ) -> str | dict[str, Any]:
        """
        Formats the call site information stored in data as a string or dictionary.

        Args:
            data:    The exception data containing the caller_info property.
            as_dict: If True, returns raw data as a dictionary (suited for LOG mode).

        Returns:
            When as_dict=False: 'File: ... | Line: ... | Path: ... | Function: ...'
            When as_dict=True:  {'file': '...', 'line': ..., 'path': '...', 'func': '...'}
        """
        # 1. Access the lazily-computed property from the data object
        caller_info = data.caller_info

        # 2. Safe handling of missing data (location disabled or not found)
        if not caller_info:
            if as_dict:
                return {"file": "unknown", "line": 0, "path": "unknown", "func": "unknown"}
            return "Location: Unknown"

        # 3. Variant for machine processing (LOG mode)
        if as_dict:
            return {
                "file": caller_info.get("file", "unknown"),
                "line": caller_info.get("line", 0),
                "path": caller_info.get("full_path", "unknown"),
                "func": caller_info.get("function", "unknown"),
            }

        # 4. Variant for human reading (PRETTY, SIMPLE, ONELINE modes)
        return " | ".join((
            f"File: {caller_info['file']}",
            f"Line: {caller_info['line']}",
            f"Path: {caller_info['full_path']}",
            f"Function: {caller_info['function']}",
        ))


_DESIGN_NOTES = """
# PrintCallerInfoMixin

## Purpose
Formats call site information (file, line, path, function) into an output 
string or dictionary. It acts as a bridge between the raw location data 
and the final visual representation.

## Data Integration
Unlike previous versions, this mixin now accepts the full `SimpleExceptionData` 
object. It relies on the `data.caller_info` property to provide the necessary 
information. This property is lazily computed by the data layer itself, 
ensuring that the location is resolved only when needed.

## The as_dict parameter
Added to support LOG mode, which uses a `key=value` format.
- `False` (default) — a formatted string for human reading.
- `True` — a raw dictionary that LOG mode assembles into its own format.

## Fallback Logic
If `data.caller_info` returns `None` (either because location reporting is 
disabled or the frame was not found), the method returns safe "unknown" 
placeholders. This prevents the entire rendering process from failing due 
to missing metadata.

## Notes
- Marked `# noinspection PyMethodMayBeStatic` — as a mixin method it must 
  be accessible via `self` in subclasses of `ModeBase`.
- Standardized API: Matches the signature pattern of other output mixins 
  (accepts `data: SimpleExceptionData`).
"""