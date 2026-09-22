from .raise_system_blacklist_mutation_error import raise_system_blacklist_mutation_error
from .raise_unknown_settings_attribute_error import raise_unknown_settings_attribute_error
from .validate_dynamic_cls_cache import validate_dynamic_cls_cache
from .validate_get_location import validate_get_location
from .validate_location_blacklist import validate_location_blacklist
from .validate_message_mode import validate_message_mode
from .validate_value_truncation_length import validate_value_truncation_length


_DESIGN_NOTES = """
# Settings Matrix Validation Sub-Package

## Purpose
Houses type-checking assertions, boundary validations, and specialized error dispatches protecting the 
integrity of the global settings configuration registry against faulty modifications.

## Internal Components Registry

| Component                                 | Type     | Description                                                                          |
| :---------------------------------------- | :------- | :----------------------------------------------------------------------------------- |
| `validate_message_mode`                   | Function | Validates that the selected rendering mode is supported.                             |
| `validate_value_truncation_length`        | Function | Validates value truncation limits and rejects invalid numeric values.                |
| `validate_get_location`                   | Function | Validates default caller-location offsets.                                           |
| `validate_location_blacklist`             | Function | Validates custom location exclusion collections.                                     |
| `validate_dynamic_cls_cache`              | Function | Ensures the dynamic class cache follows the expected storage schema.                 |
| `raise_system_blacklist_mutation_error`   | Function | Prevents modification of protected internal blacklist entries.                       |
| `raise_unknown_settings_attribute_error`  | Function | Raises an internal error when an unknown settings attribute is modified.             |
"""