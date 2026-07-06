from typing import Any, Protocol, Self, runtime_checkable
from simplibs.sentinels import UNSET, UnsetType
from .SimpleExceptionDataProtocol import SimpleExceptionDataProtocol


@runtime_checkable
class SimpleExceptionProtocol(SimpleExceptionDataProtocol, Protocol):
    """
    Protocol defining the full public interface of SimpleException.

    Inherits all data attributes and properties from SimpleExceptionDataProtocol.
    """

    # --- Additional exception-specific fields ---
    rendered_message: str

    # -------------------------------------------------------------------------
    # Dunder / Magic methods (from Exception and Custom)
    # -------------------------------------------------------------------------

    def __init__(
        self,
        message: str | None = None,
        *,
        value: Any = UNSET,
        label: str | None = None,
        expected: str | None = None,
        problem: str | tuple[str, ...] | list[str] | None = None,
        context: str | tuple[str, ...] | list[str] | None = None,
        how_to_fix: str | tuple[str, ...] | list[str] | None = None,
        error_name: str | None = None,
        exception: Exception | type[Exception] | None = None,
        get_location: bool | int | None = None,
        skip_locations: tuple[str, ...] | str | None = None,
        oneline: bool = False,
    ) -> None: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

    # -------------------------------------------------------------------------
    # Transformators
    # -------------------------------------------------------------------------

    def with_location_offset(self, offset: int = 1) -> Self:
        """Creates a new exception instance with increased get_location depth."""
        ...