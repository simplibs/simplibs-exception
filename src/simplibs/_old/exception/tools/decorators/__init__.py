from .raise_location_offset import raise_location_offset


_DESIGN_NOTES = """
# tools/decorators

## Contents
Specialized decorators for exception handling and manipulation.

| Decorator               | Description                                           |
|-------------------------|-------------------------------------------------------|
| `raise_location_offset` | Catches exceptions and re-targets their stack origin. |

## Responsibility
Decorators in this package provide a declarative way to manage how exceptions 
report their location. This is essential for clean APIs where internal 
validation logic should be hidden from the end-user's traceback.
"""