from .SimpleException import SimpleException


_DESIGN_NOTES = """
# exception

## Contents
The core class of the ecosystem — a structured exception combining the data
layer, validation, normalisation, and output modes.

| Name             | Description                                                      |
|------------------|------------------------------------------------------------------|
| `SimpleException`| Core class — the foundation for all exceptions in the Simple ecosystem |

## Usage
```python
from simple_exception.exception import SimpleException

raise SimpleException(
    value_label = "parameter age",
    expected    = "a positive integer",
    value       = age,
    problem     = "value is negative",
    how_to_fix  = "Provide a value greater than 0.",
)
```
"""