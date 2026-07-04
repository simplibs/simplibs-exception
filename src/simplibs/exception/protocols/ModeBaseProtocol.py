from typing import Protocol, runtime_checkable, TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from .SimpleExceptionDataProtocol import SimpleExceptionDataProtocol


@runtime_checkable
class ModeBaseProtocol(Protocol):
    """
    Comprehensive protocol mirroring the entire contract of an exception mode.
    Used for full-spectrum type hinting and internal code intelligence.
    """

    def render(
        self,
        data: "SimpleExceptionDataProtocol",
        *,
        validate: bool = True
    ) -> str:
        """Public entry point with built-in validation."""
        ...

    def _render(self, data: "SimpleExceptionDataProtocol") -> str:
        """Internal abstract method defining the specific text layout."""
        ...

    def __repr__(self) -> str: ...