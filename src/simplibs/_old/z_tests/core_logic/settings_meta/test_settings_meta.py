from typing import Any, Callable
# Inners
from .validations import (
    validate_dynamic_cls_cache,
    validate_get_location,
    validate_location_blacklist,
    validate_message_mode,
    validate_value_truncation_length,
    raise_system_blacklist_mutation_error,
    raise_unknown_settings_attribute_error
)


class SettingsMeta(type):
    """Metaclass for validating attribute assignments on SimpleExceptionSettings."""

    # --- Mapping of attribute names to their validators ---
    _VALIDATORS: dict[str, Callable[[Any], None]] = {
        "GET_LOCATION": validate_get_location,
        "LOCATION_BLACKLIST": validate_location_blacklist,
        "MESSAGE_MODE": validate_message_mode,
        "VALUE_TRUNCATION_LENGTH": validate_value_truncation_length,
        "_dynamic_cls_cache": validate_dynamic_cls_cache,
    }

    # --- Setter that intercepts and validates all configuration modifications ---
    def __setattr__(
        cls,
        name: str,
        value: Any
    ) -> None:
        # 1. Strict guard against modifying protected system metadata
        if name == "_SYSTEM_BLACKLIST":
            raise_system_blacklist_mutation_error(value)

        # 2. Verify that the attribute is known and permitted
        if name not in cls._VALIDATORS:
            raise_unknown_settings_attribute_error(cls, name)

        # 3. Fire the designated contextual validation algorithm
        cls._VALIDATORS[name](value)

        # 4. Commit the validated payload back into the core namespace memory stream
        super().__setattr__(name, value)


_DESIGN_NOTES = """
# SettingsMeta

## Purpose
The operational metaclass driving `SimpleExceptionSettings`. It provides an interceptive hardware-like 
validation layer guarding the global framework settings namespace against structural type pollution, 
invalid configurations, and hazardous attribute typos.

## Decoupled Error Architecture
To preserve high scannability and separate core execution flows from text formatting, all exception 
generation mechanics for structural violations (`_SYSTEM_BLACKLIST` mutations and Unknown Typo attributes) 
are delegated to dedicated error-raiser modules (`raise_...`). These functions use Python's strict `NoReturn` 
signature patterns, ensuring that terminal paths are cleanly flagged for both developers and static analyzers.

## Core Mechanisms
1. **System Protection**: intercept variables matching `_SYSTEM_BLACKLIST`, preventing manual alteration.
2. **Strict White-Listing**: Validates incoming names against the keys of `_VALIDATORS`.
3. **Dynamic Dispatch**: Passes valid payloads to the corresponding standalone validation component.
"""