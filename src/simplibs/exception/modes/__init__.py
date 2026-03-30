from .PRETTY import PRETTY, PrettyMessage
from .SIMPLE import SIMPLE, SimpleMessage
from .ONELINE import ONELINE, OnelineMessage
from .LOG import LOG, LogMessage
from .base_class import ModeBase


_DESIGN_NOTES = """
# modes

## Contents
Output modes for `SimpleException` — each mode defines how the exception
is displayed. Used either directly or via `SimpleExceptionSettings.DEFAULT_MESSAGE_MODE`.

| Instance  | Class           | Description                                           |
|-----------|-----------------|-------------------------------------------------------|
| `PRETTY`  | `PrettyMessage` | Structured output framed with double separator lines  |
| `SIMPLE`  | `SimpleMessage` | Plain text output without decorations                 |
| `ONELINE` | `OnelineMessage`| Compact single-line output                            |
| `LOG`     | `LogMessage`    | Key=value format for log parsers                      |

## Custom mode
```python
from simple_exception.modes import ModeBase

class MyMode(ModeBase):
    def _full_outcome(self, data, caller_info):
        return f"[{data.error_name}] {data.message}"

MY_MODE = MyMode()
```
"""