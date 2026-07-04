from .WithLocationOffset import WithLocationOffsetMixin


_DESIGN_NOTES = """
# _exception_mixins/transformators

## Contents
Mixins designed to create modified versions of the current exception instance.

| Mixin                      | Method                   | Description                                         |
|----------------------------|--------------------------|-----------------------------------------------------|
| `WithLocationOffsetMixin`  | `with_location_offset()` | Returns a new instance with a shifted stack depth   |

## Responsibility
Transformators handle the "evolution" of an exception. They allow developers 
to take an existing error and adjust its metadata (like the reported location) 
before re-raising it, which is essential for building clean, user-friendly 
library wrappers.
"""