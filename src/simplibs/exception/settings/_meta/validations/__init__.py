from .SimpleExceptionSettingsError import SimpleExceptionSettingsError
from .validate_get_location import validate_get_location
from .validate_location_blacklist import validate_location_blacklist
from .validate_message_mode import validate_message_mode
from .validate_dynamic_cls_cache import validate_dynamic_cls_cache


_DESIGN_NOTES = """
# settings/_meta/validations

## Contents
Validation functions for the individual attributes of `SimpleExceptionSettings`
and the grouped exception for settings-related errors.

| Name                           | Description                                          |
|--------------------------------|------------------------------------------------------|
| `SimpleExceptionSettingsError` | Grouped exception for settings-related errors        |
| `validate_get_location`        | Verifies that the value is an `int` or `bool`        |
| `validate_location_blacklist`  | Verifies that the value is a `tuple[str, ...]`       |
| `validate_message_mode`        | Verifies that the value is a `ModeBase` instance     |
| `validate_dynamic_cls_cache`   | Permits only an empty dict — cache reset only        |
"""