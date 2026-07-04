from .base_class import ModeBase
from .LOG import LOG
from .ONELINE import ONELINE
from .PRETTY import PRETTY
from .SIMPLE import SIMPLE

__all__ = [
    "LOG",
    "ModeBase",
    "ONELINE",
    "PRETTY",
    "SIMPLE",
]


_DESIGN_NOTES = """
# Rendering Modes Core Package Entry Point

## Purpose
This package acts as the authoritative orchestration suite managing exception string serialization models. 
It houses and exports both the abstract foundational blueprint and the four pre-configured production-ready 
singleton engine matrices.

## Exported Registry

| Component  | Type             | Description                                                                         |
| :--------- | :--------------- | :---------------------------------------------------------------------------------- |
| `PRETTY`   | Singleton Engine | Fully bordered, high-density terminal renderer optimized for interactive debugging. |
| `SIMPLE`   | Singleton Engine | Clean text renderer without decorative layout elements.                             |
| `ONELINE`  | Singleton Engine | Compact single-line renderer for concise output.                                    |
| `LOG`      | Singleton Engine | Key-value renderer tailored for structured logging systems.                         |
| `ModeBase` | Abstract Class   | Base contract for implementing custom exception rendering engines.                  |

## Architectural Layout Isolation
While the sub-directories `printers/` carry out the low-level string manipulation routines, this root 
namespace exposes only the fully compiled, active render singletons. This design protects client modules 
from inner pipeline fragmentation and preserves a clean Flat API surface on the library's root boundary.
"""