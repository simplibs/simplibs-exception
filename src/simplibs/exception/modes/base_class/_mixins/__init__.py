from .PrintCallerInfo import PrintCallerInfoMixin
from .PrintIntroLine import PrintIntroLineMixin
from .PrintValueWithType import PrintValueWithTypeMixin


_DESIGN_NOTES = """
# modes/base_class/_mixins

## Contents
Helper mixins for assembling individual parts of the output string.
Used exclusively by `ModeBase`.

| Mixin                    | Method                   | Output                              |
|--------------------------|--------------------------|-------------------------------------|
| `PrintCallerInfoMixin`   | `_print_caller_info`     | File: ... | Line: ... | Path: ...   |
| `PrintIntroLineMixin`    | `_print_intro_line`      | ⚠️ ERROR_NAME: value_label          |
| `PrintValueWithTypeMixin`| `_print_value_with_type` | "value" (type)                      |
"""