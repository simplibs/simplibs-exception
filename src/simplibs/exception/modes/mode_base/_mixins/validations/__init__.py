from .validate_has_simple_exception_data import validate_has_simple_exception_data


_DESIGN_NOTES = """
# modes/base_class/_validations

## Contents
Validation logic for `ModeBase`. Placed here because `ModeBase` is the
sole consumer.

| Name                                | Description                                          |
|-------------------------------------|------------------------------------------------------|
| `validate_has_simple_exception_data`| Verifies that the data inherits from `SimpleExceptionData` |
"""