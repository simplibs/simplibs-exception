from typing import Any, NoReturn
# Outers
from ...._core_logic.internal_exceptions import SimpleExceptionSettingsError


def raise_system_blacklist_mutation_error(
    value: Any
) -> NoReturn:
    """Explicitly raises an error when an attempt is made to mutate the internal read-only system blacklist."""
    raise SimpleExceptionSettingsError(
        value=value,
        label="SimpleExceptionSettings",
        problem="The protected '_SYSTEM_BLACKLIST' attribute is strict read-only metadata.",
        how_to_fix=(
            "Do not attempt to alter the core framework system-level blacklist.",
            "To skip your custom repository paths or wrapper files, append them to: "
            "SimpleExceptionSettings.LOCATION_BLACKLIST",
        ),
    )


_DESIGN_NOTES = """
# raise_system_blacklist_mutation_error

## Purpose
A specialized architectural execution stopper (Error Raiser) that triggers whenever a write operation 
targets the immutable system telemetry layout boundary (`_SYSTEM_BLACKLIST`).

## Design Pattern
By decoupling the text composition matrix from `SettingsMeta.__setattr__`, we keep the meta dispatcher 
clean and highly readable. Utilizing `NoReturn` informs the static compiler that this path is terminal.
"""