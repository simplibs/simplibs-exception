from typing import TYPE_CHECKING
# Outers
from ....SimpleExceptionSettings import SimpleExceptionSettings as S
# Annotations
if TYPE_CHECKING:
    from ....protocols import SimpleExceptionDataProtocol


def assemble_message(
    instance: "SimpleExceptionDataProtocol",
    oneline: bool
) -> str:
    """
    Evaluates configuration flags and dispatches the exception data to the
    active rendering engine mode to build the final string message.
    """
    # 1. If oneline mode is requested, intercept and use the specialized ONELINE mode
    if oneline:
        from ....modes import ONELINE  # Local import prevents circular dependency
        return ONELINE.render(instance, validate=False)

    # 2. Otherwise, fall back to the globally configured message mode from settings
    return S.MESSAGE_MODE.render(instance, validate=False)


_DESIGN_NOTES = """
# assemble_message

## Purpose
Acts as the central dispatcher between `SimpleException.__init__` and the 
rendering engine (`modes`). It determines which formatting layout should be 
applied to the exception's data fields and returns the final assembled text string.

## Circular Dependency Prevention
The import statement `from ...modes import ONELINE` is deliberately placed 
inside the execution block of the `if oneline:` condition. 
Because the `modes` package requires access to `SimpleException` (or its data protocols) 
for structural type checking, a standard top-level import would cause a fatal 
circular import error at runtime. Deferring the import until the exception is 
actually instantiated completely bypasses this limitation.

## Nomenclature (Why 'assemble_message' and 'render'?)
To maintain a clean architectural separation, the responsibilities are named distinctively:
- **`assemble_message`** (this function): Does not format text itself. It evaluates 
  state context (`oneline` flag vs. global settings) and orchestrates *which* tool to use.
- **`render`** (method on `ModeBase` subclasses): The actual concrete implementation 
  that formats, pads, and chains strings together into the final payload.

## Usage
Invoked at the very end of `SimpleException.__init__` right before calling the 
native `Exception.__init__`:
```python
self.rendered_message = assemble_message(self, oneline)
Exception.__init__(self, self.rendered_message)
"""