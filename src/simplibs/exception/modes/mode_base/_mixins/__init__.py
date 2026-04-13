from .PrintCallerInfo import PrintCallerInfoMixin
from .PrintIntroLine import PrintIntroLineMixin
from .PrintValueWithType import PrintValueWithTypeMixin
from .RenderMessage import RenderMessageMixin


_DESIGN_NOTES = """
# modes/base_class/_mixins

## Contents
Helper mixins for handling the rendering workflow and assembling individual 
parts of the output string. These are used to compose the `ModeBase` class.

| Mixin                      | Primary Method           | Responsibility                                  |
|----------------------------|--------------------------|-------------------------------------------------|
| `RenderMessageMixin`       | `render_message`         | Orchestrates workflow, validation, and dispatch |
| `PrintCallerInfoMixin`     | `_print_caller_info`     | Formats: File: ... | Line: ... | Path: ...     |
| `PrintIntroLineMixin`      | `_print_intro_line`      | Formats: ⚠️ ERROR_NAME: value_label            |
| `PrintValueWithTypeMixin`  | `_print_value_with_type` | Formats: "value" (type)                        |

## Architecture Note
`RenderMessageMixin` acts as the "brain" of the operation, determining which 
scenario (Empty, Message, or Full) to execute. The other mixins provide 
specialized formatting tools that the actual Mode implementations use to 
build their specific output strings.
"""