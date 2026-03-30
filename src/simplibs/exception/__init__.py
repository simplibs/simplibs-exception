from .exception import SimpleException
from .utils import bool_or_exception, extract_caller_info
from .modes import PRETTY, SIMPLE, ONELINE, LOG, ModeBase
from .settings import SimpleExceptionSettings, SimpleExceptionSettingsError


__all__ = [
    # Core class
    "SimpleException",
    # Utils
    "bool_or_exception",
    "extract_caller_info",
    # Modes
    "PRETTY",
    "SIMPLE",
    "ONELINE",
    "LOG",
    "ModeBase",
    # Settings
    "SimpleExceptionSettings",
    "SimpleExceptionSettingsError",
]


_DESIGN_NOTES = """
# simple_exception

## Public API
| Name                           | Description                                                       |
|--------------------------------|-------------------------------------------------------------------|
| `SimpleException`              | Core class — the foundation for all exceptions in the ecosystem   |
| `bool_or_exception`            | Shortcut for conditional exception raising                        |
| `extract_caller_info`          | Utility for retrieving call site information from the stack       |
| `PRETTY`                       | Default mode — structured output with separator lines             |
| `SIMPLE`                       | Plain text output without decorations                             |
| `ONELINE`                      | Compact single-line output                                        |
| `LOG`                          | Key=value format for log parsers                                  |
| `ModeBase`                     | Base class for custom modes                                       |
| `SimpleExceptionSettings`      | Central configuration of the library                              |
| `SimpleExceptionSettingsError` | Exception for errors when changing settings                       |
"""