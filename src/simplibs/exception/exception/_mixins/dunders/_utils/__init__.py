from .check_children_class_attributes import check_children_class_attributes


_DESIGN_NOTES = """
# exception/_mixins/dunders/_utils

## Contents
An internal utility for validating subclasses at definition time.
Used exclusively by `DunderInitSubclassMixin`.

| Name                              | Description                                          |
|-----------------------------------|------------------------------------------------------|
| `check_children_class_attributes` | Verifies a subclass's attributes and types against the parent |
"""