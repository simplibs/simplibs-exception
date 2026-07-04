from typing import Any, Protocol, runtime_checkable
from simplibs.sentinels import UnsetType


@runtime_checkable
class SimpleExceptionDataProtocol(Protocol):
    """Protocol defining the public interface of SimpleExceptionData."""

    # --- Core exception info ---
    error_name: str
    exception: type[Exception] | None
    intercepted_exception: str | None

    # --- Info about the inspected value ---
    value: object | UnsetType
    label: str | None

    # --- Exception description ---
    expected: str | None
    message: str | None
    problem: str | tuple[str, ...] | None
    context: str | tuple[str, ...] | None

    # --- How to fix ---
    how_to_fix: str | tuple[str, ...] | None

    # --- Location info ---
    get_location: int | bool
    skip_locations: tuple[str, ...]
    _cached_caller_info: dict[str, Any] | None | UnsetType

    # --- Single-line output ---
    oneline: bool

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def caller_info(self) -> dict[str, Any] | None:
        """
        Lazily-computed and cached call site information.
        Returns a dictionary with keys (file, path, line, function) or None.
        """
        ...

    # -------------------------------------------------------------------------
    # Serializers
    # -------------------------------------------------------------------------

    def to_dict(self: "SimpleExceptionDataProtocol") -> dict[str, Any]:
        """Serializes core public exception attributes into a clean dictionary — UNSET values are omitted."""
        ...

    def to_debug_dict(self: "SimpleExceptionDataProtocol") -> dict[str, Any]:
        """Compiles a comprehensive diagnostic snapshot dictionary including computed metadata."""
        ...

    def to_json(self: "SimpleExceptionDataProtocol") -> str:
        """Serializes core instance public data fields into an un-indented JSON string representation."""
        ...