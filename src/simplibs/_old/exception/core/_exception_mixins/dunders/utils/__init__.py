from .check_children_class_attributes import check_children_class_attributes

_DESIGN_NOTES = """
# dunders/utils

## Contents
Utility functions specifically designed for dunder method mixins.

| Name                               | Description                                           |
|------------------------------------|-------------------------------------------------------|
| `check_children_class_attributes`  | Validates subclass attributes against parent annotations|

## Responsibility
This package hosts private utilities for the `dunders` package. These utilities 
are not intended to be used by the rest of the library or by the end user.
"""