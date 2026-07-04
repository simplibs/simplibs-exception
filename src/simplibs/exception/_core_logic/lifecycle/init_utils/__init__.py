from .assemble_message import assemble_message
from .normalize_bool import normalize_bool
from .normalize_exception import normalize_exception
from .normalize_string import normalize_string
from .normalize_strings import normalize_strings
from .process_get_location import process_get_location
from .process_skip_locations import process_skip_locations


_DESIGN_NOTES = """
# Initialization Utilities Sub-Package

## Purpose
Provides sanitization, transformation, and normalization helpers executed during the constructor phase 
of an exception instantiation to clear input variants before storage.

## Internal Components Registry

| Component                  | Type     | Description                                                                                 |
| :------------------------- | :------- | :------------------------------------------------------------------------------------------ |
| `assemble_message`         | Function | Builds the final textual exception message from normalized components.                      |
| `normalize_bool`           | Function | Normalizes truthy and falsy values into strict booleans.                                    |
| `normalize_string`         | Function | Cleans and normalizes a single text value.                                                  |
| `normalize_strings`        | Function | Converts collections of text values into normalized immutable tuples.                       |
| `normalize_exception`      | Function | Normalizes or unwraps intercepted exception objects.                                        |
| `process_get_location`     | Function | Resolves stack depth values used for automatic caller detection.                            |
| `process_skip_locations`   | Function | Merges user-defined exclusion rules with the framework's internal skip locations.           |
"""