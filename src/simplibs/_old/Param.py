from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True, init=False)
class Param:
    """Explicit semantic wrapper isolating a single parameter payload.

    Prevents unexpected collection unpacking inside the parameter normalization
    pipeline (`process_params`). Enforces that the encapsulated value—regardless of
    whether it is a tuple, list, or set—is treated strictly as a singular,
    indivisible positional argument.

    Example:
        valid_input = Param(("a.py", "b.py"))
        invalid_param = (Param((1, 2, 3)), Kwargs(strict=True))
    """

    value: Any

    def __init__(
        self,
        value: Any
    ) -> None:
        """Initialize the isolated parameter container.

        Args:
            value: The raw parameter payload to protect from pipeline unpacking.
        """
        object.__setattr__(self, "value", value)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value!r})"


_DESIGN_NOTES = """
# Param (Semantic Argument Isolation Guard)

## Purpose
An architectural token wrapper designed to protect complex collections from accidental signature 
unpacking across automated test runners. It signals the parameter evaluation lifecycle (`process_params`) 
that its contents represent a single, atomic positional argument, resolving the implicit ambiguity 
of native Python sequences (`tuple` / `list`) within dynamic matrix routers.

## Structural Strategy
Unlike `Kwargs` or multi-positional unpackers, `Param` does not implement dictionary or sequence 
protocols. It acts strictly as a rigid, transparent box with a single immutable `.value` property. 
This minimalist footprint guarantees that it cannot be accidentally iterated over or mutated 
during transport.

## Pipeline Integration
When the normalization utility encounters a `Param` token (either standalone or nested inside a 
standard routing tuple), it immediately calls `.value` to extract the payload, bypassing the 
sequence flattening loops. This provides developers with an explicit mechanism to test methods 
that accept raw containers as individual arguments.
"""