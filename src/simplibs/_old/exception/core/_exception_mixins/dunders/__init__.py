from .InitSubclass import DunderInitSubclassMixin
from .New import DunderNewMixin

_DESIGN_NOTES = """
# _exception_mixins/dunders

## Contents
Mixins that hook into Python's dunder methods to manage class lifecycle and 
dynamic inheritance.

| Name                      | Method               | Purpose                                         |
|---------------------------|----------------------|-------------------------------------------------|
| `DunderInitSubclassMixin` | `__init_subclass__`  | Validation of subclasses at definition time     |
| `DunderNewMixin`          | `__new__`            | Dynamic MRO injection and class-level caching   |

## Usage
These mixins are inherited by the main `SimpleException` class. They ensure 
that every exception is both correctly defined (no typos) and correctly 
instantiated (proper inheritance chain).
"""