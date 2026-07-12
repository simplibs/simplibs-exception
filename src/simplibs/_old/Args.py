from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Iterator, overload


@dataclass(slots=True, frozen=True, init=False)
class Args(Sequence[Any]):
    """Explicit semantic wrapper distinguishing multi-positional arguments from literal sequences.

    Prevents type ambiguity inside the parameter normalization pipeline by ensuring
    that wrapped elements are strictly expanded into positional parameters (*args) rather
    than evaluated as a single collective collection container.

    Example:
        invalid_param = Args(MockClass, "bad-value")
        invalid_param = Args(("a.py", "b.py"))  # Wraps a single tuple parameter cleanly if needed
    """

    _values: tuple[Any, ...]

    def __init__(
        self,
        *args: Any
    ) -> None:
        """Initialize the multi-positional argument storage layer.

        Captures all provided inline positional payloads into an immutable tuple layout.

        Args:
            *args: Dynamic inline positional parameters to form the execution chain.
        """
        object.__setattr__(self, "_values", args)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    @overload
    def __getitem__(self, index: int) -> Any: ...

    @overload
    def __getitem__(self, index: slice) -> tuple[Any, ...]: ...

    def __getitem__(self, index: int | slice) -> Any:
        # noinspection PyTypeChecker
        return self._values[index]

    def __repr__(self) -> str:
        inner = ", ".join(repr(v) for v in self._values)
        return f"{type(self).__name__}({inner})"


_DESIGN_NOTES = """
# Args (Semantic Invocation Wrapper)

## Purpose
An architectural token wrapper designed to bypass positional collection ambiguity across automated 
test runners. It explicitly informs parameter evaluation pipelines (`manage_param`) that the encapsulated 
sequence sequence must be unpacked into individual positional arguments (`*args`), resolving the structural 
collision where a raw tuple or list is intended to be evaluated as a single collective parameter.

## Initialization Mechanics
The constructor uses Python's standard splat operator (`*args`) to catch all incoming comma-separated 
arguments inline. These captured nodes are immediately committed into a protected, frozen tuple registry. 
Unlike `Kwargs`, there are no type-guard constraints needed here, as any arbitrary sequence of core types, 
objects, or collections represents a structurally valid positional stack.

## Dunder API Integrity & Sequence Polymorphism
By inheriting from `collections.abc.Sequence` and satisfying the core abstract methods (`__iter__`, 
`__len__`, `__getitem__`), the `Args` instance achieves native sequence polymorphism. It behaves 
as an unmodifiable, frozen tuple token. This guarantees it can be seamlessly evaluated, sliced, 
or explicitly expanded anywhere inside python core execution spaces using standard single-asterisk triggers:
`func(*Args(a, b, c))`.
"""