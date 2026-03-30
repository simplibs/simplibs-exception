from .InitSubclass import DunderInitSubclassMixin
from .New import DunderNewMixin


_DESIGN_NOTES = """
# exception/_mixins/dunders

## Contents
Mixins for the dunder methods of `SimpleException`.

| Name                      | Method               | Description                                          |
|---------------------------|----------------------|------------------------------------------------------|
| `DunderInitSubclassMixin` | `__init_subclass__`  | Validates subclasses at definition time              |
| `DunderNewMixin`          | `__new__`            | Dynamically adds an exception type to instance ancestors |
"""