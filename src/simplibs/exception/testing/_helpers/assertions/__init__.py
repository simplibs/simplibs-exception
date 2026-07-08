from .check_exception_fields import check_exception_fields
from .compare_strings import compare_strings
from .manage_param import manage_param


_DESIGN_NOTES = """
# Testing Assertions Low-Level Engine

## Purpose
Consolidates individual data checking blocks, string normalization layers, and signature parameters 
unbackers used to audit runtime property allocations on instantiated exceptions.

## Internal Components Registry

| Component                | Type     | Description                                                                          |
| :----------------------- | :------- | :----------------------------------------------------------------------------------- |
| `check_exception_fields` | Function | Validates exception attributes against expected values and conditions.               |
| `compare_strings`        | Function | Performs exact or partial string matching for validation purposes.                   |
| `manage_param`           | Function | Normalizes and prepares dynamic test parameters for execution and validation.         |
"""