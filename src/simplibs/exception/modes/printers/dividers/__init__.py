from .DOT_PREFIX import DOT_PREFIX
from .DOUBLE_LINE import DOUBLE_LINE
from .EMPTY_PREFIX import EMPTY_PREFIX
from .SINGLE_LINE import SINGLE_LINE

__all__ = [
    "DOT_PREFIX",
    "DOUBLE_LINE",
    "EMPTY_PREFIX",
    "SINGLE_LINE",
]


_DESIGN_NOTES = """
# Formatting Dividers Sub-Package

## Purpose
This package houses static string configuration constants and prefix rules used to separate 
and border individual blocks within the rendered exception frame layouts.

## Exported Registry

| Component      | Type            | Description                                                                      |
| :------------- | :-------------- | :------------------------------------------------------------------------------- |
| `DOUBLE_LINE`  | String Constant | Double horizontal divider line used for framing outer boundaries.                |
| `SINGLE_LINE`  | String Constant | Single horizontal divider line separating internal layout segments.              |
| `DOT_PREFIX`   | String Constant | Pre-formatted dot-bullet layout prefix for indentation alignment.                |
| `EMPTY_PREFIX` | String Constant | Pure whitespace padding block ensuring text alignment parity.                    |
"""