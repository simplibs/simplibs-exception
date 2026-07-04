from .init_subclass import _type_matches, check_children_attributes
from .init_utils import (
    assemble_message,
    normalize_bool,
    normalize_exception,
    normalize_string,
    normalize_strings,
    process_get_location,
    process_skip_locations,
)
from .new_method import add_exception_type


_DESIGN_NOTES = """
# Master Exception Lifecycle Orchestration Sub-Package

## Purpose
Consolidates the complete sequence of allocation, construction, normalization, and verification steps 
governing how an exception instance is brought to life and securely configured.

## Internal Sub-Module Aggregation

| Category              | Components                                    | Description                                                                  |
| :-------------------- | :-------------------------------------------- | :--------------------------------------------------------------------------- |
| **New Method**        | `add_exception_type`                          | Dynamic exception type creation and class caching.                           |
| **Init Utils**        | `assemble_message`, `normalize_*`, `process_*` | Input normalization, validation, and caller resolution utilities.            |
| **Init Subclass**     | `check_children_attributes`, `_type_matches`  | Inheritance validation and subclass consistency checks.                      |
"""