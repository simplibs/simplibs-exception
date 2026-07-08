from typing import TYPE_CHECKING, NoReturn
# Outers
from ....core_logic.internal_exceptions import SimpleExceptionSettingsError
# Annotations
if TYPE_CHECKING:
    from ..SettingsMeta import SettingsMeta


def raise_unknown_settings_attribute_error(
    cls: "SettingsMeta",
    name: str
) -> NoReturn:
    """Explicitly raises an error when an unauthorized or typo-polluted attribute name is assigned to Settings."""
    permitted_keys = [k for k in cls._VALIDATORS if not k.startswith("_")]

    raise SimpleExceptionSettingsError(
        value=name,
        label="SimpleExceptionSettings",
        expected=f"one of the permitted attributes: {permitted_keys}",
        problem="unknown attribute — likely a typo or a new attribute missing its validator",
        how_to_fix=(
            "Check for a typo — the permitted operational attributes are listed under 'Expected'.",
            "If introducing a new setting, register its corresponding validation block inside _VALIDATORS.",
        ),
    )


_DESIGN_NOTES = """
# raise_unknown_settings_attribute_error

## Purpose
A specialized error execution stopper triggered when a developer attempts to write a non-whitelisted 
attribute key or introduces a typo into the global configuration namespace.

## Dynamic Reflection
The function receives the metaclass instance context (`cls`) to dynamically extract and format the 
active keys from `_VALIDATORS` for the user's `expected` layout field. This guarantees that the 
error message updates automatically if new settings are introduced to the ecosystem.
"""