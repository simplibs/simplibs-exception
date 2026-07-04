from typing import Any, Protocol, runtime_checkable, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .ModeBaseProtocol import ModeBaseProtocol


@runtime_checkable
class SimpleExceptionSettingsProtocol(Protocol):
    """
    Protocol defining the structure and interface of SimpleExceptionSettings.

    Since this class is a pure configuration registry not intended for
    instantiation, the protocol covers its class-level attributes and methods.
    """

    # --- System Blacklist (Read-Only) ---
    _SYSTEM_BLACKLIST: tuple[str, ...]

    # --- Default configuration attributes ---
    DEFAULT_GET_LOCATION: int | bool
    DEFAULT_LOCATION_BLACKLIST: tuple[str, ...]
    DEFAULT_MESSAGE_MODE: "ModeBaseProtocol"
    DEFAULT_VALUE_TRUNCATION_LENGTH: int

    # --- Internal cache ---
    _dynamic_cls_cache: dict[tuple[Any, ...], type[BaseException]]

    # -------------------------------------------------------------------------
    # Initialization and Lifecycle
    # -------------------------------------------------------------------------

    def __init__(self) -> None:
        """
        Initialization always raises SimpleExceptionSettingsError
        as this class is not intended to be instantiated.
        """
        ...

    @classmethod
    def reset(cls) -> None:
        """Resets all settings back to their factory default values."""
        ...