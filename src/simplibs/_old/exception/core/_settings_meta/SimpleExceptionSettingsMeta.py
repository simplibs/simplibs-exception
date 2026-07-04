# Outers
from .._internal_exceptions import SimpleExceptionSettingsError
# Inners
from .validations import (
    validate_get_location,
    validate_location_blacklist,
    validate_message_mode,
    validate_dynamic_cls_cache,
    validate_value_truncation_length,
)


class SimpleExceptionSettingsMeta(type):
    """Metaclass for validating attribute assignments on SimpleExceptionSettings."""

    # --- Mapping of attribute names to their validators ---
    _VALIDATORS = {
        "DEFAULT_GET_LOCATION": lambda v: validate_get_location(v),
        "DEFAULT_LOCATION_BLACKLIST": lambda v: validate_location_blacklist(v),
        "DEFAULT_MESSAGE_MODE": lambda v: validate_message_mode(v),
        "DEFAULT_VALUE_TRUNCATION_LENGTH": lambda v: validate_value_truncation_length(v),
        "_dynamic_cls_cache": lambda v: validate_dynamic_cls_cache(v),
    }

    # --- Setter that only accepts defined attribute names ---
    def __setattr__(cls, name: str, value) -> None:
        if name not in cls._VALIDATORS:
            raise SimpleExceptionSettingsError(
                value=name,
                value_label="SimpleExceptionSettings",
                expected=f"one of the permitted attributes: {[k for k in cls._VALIDATORS if not k.startswith('_')]}",
                problem="unknown attribute — likely a typo or a new attribute missing its validator",
                how_to_fix=(
                    "Check for a typo — the permitted attributes are listed under 'Expected'.",
                    "If adding a new attribute, register its validator in _VALIDATORS in the Meta class.",
                ),
            )
        cls._VALIDATORS[name](value)
        super().__setattr__(name, value)


_DESIGN_NOTES = """
# SimpleExceptionSettingsMeta

## Purpose
The metaclass for `SimpleExceptionSettings` — ensures that every attempt to
set a class attribute goes through validation. Guards against both typos in
attribute names and invalid values being assigned.

## _VALIDATORS
The mapping is the core element of the entire validation logic — it serves
two roles:

1. **White-list of permitted attributes** — only keys present here are accepted.
   Any attempt to write an unknown attribute (like a typo `DEFAULT_LOG_LOCATION`) 
   is immediately rejected. This prevents silent failures where the library 
   would ignore the setting and use the old value.

2. **Reference to the validation function** — each permitted attribute has an
   assigned function that verifies the type and validity of the provided value.
   Validation functions are defined in separate files in the `validations/`
   directory.

When extending the library with a new attribute in `SimpleExceptionSettings`,
a corresponding entry must always be added to `_VALIDATORS` — otherwise any
attempt to set that attribute will be rejected.

## __setattr__
Intercepts every write on the `SimpleExceptionSettings` class and:
1. Verifies that the attribute name is listed in `_VALIDATORS`.
2. Calls the corresponding validation function.
3. Only after successful validation passes the write through via
   `super().__setattr__`.

When listing permitted attributes in the exception message, entries prefixed
with an underscore are intentionally excluded — they are not intended for
regular use and displaying them would unnecessarily confuse the user.

## Design Rule: One Validator per Attribute
Every setting must have its own validator (even if simple). This ensures that 
we can provide very specific `how_to_fix` instructions for each individual 
configuration parameter, staying true to the library's philosophy of helpful 
error messages.
"""