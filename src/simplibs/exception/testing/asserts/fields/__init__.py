from .assert_exception_fields import assert_exception_fields

__all__ = [
    "assert_exception_fields",
]

_DESIGN_NOTES = """
# Asserts Fields Sub-Engine Registry

## Purpose
Consolidates single-responsibility assertion blades focused on evaluating the granular, 
instantiated telemetry dataset directly attached to exception objects.

## Internal Components Registry

| Component                 | Type             | Description                                                           |
| :------------------------ | :--------------- | :-------------------------------------------------------------------- |
| `assert_exception_fields` | Field Validation | Validates required fields directly on instantiated exception objects. |
"""