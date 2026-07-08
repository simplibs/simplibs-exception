from typing import TYPE_CHECKING, Any
# Annotations
if TYPE_CHECKING:
    from ....protocols import SimpleExceptionDataProtocol


def normalize_strings(
    instance: "SimpleExceptionDataProtocol",
    value: Any,
    attr: str
) -> tuple[str, ...] | str | None:
    """
    Processes a descriptive parameter (problem, context, how_to_fix) provided
    as a str, tuple, or list, and normalizes it into a flat str or a tuple[str, ...].
    """
    # 1. Process a string (return instantly as a flat single-line string)
    if isinstance(value, str):
        return value

    # 2. Process a tuple or list — retains only non-empty, stripped str items
    if isinstance(value, (tuple, list)):
        strings = [i for i in value if isinstance(i, str) and i.strip()]
        if strings:
            # Optimization: If the collection contains only one line, flatten it to str
            return strings[0] if len(strings) == 1 else tuple(strings)

    # 3. Fall back to the class-level default for the given attribute
    return getattr(instance.__class__, attr, None)


_DESIGN_NOTES = """
# normalize_strings

## Purpose
Processes and standardizes multi-line sensitive diagnostic parameters (`problem`, `context`, 
`how_to_fix`), which may be provided by the consumer as a `str`, `tuple[str, ...]`, 
or `list[str]`. It normalizes them into a highly optimized runtime state representation: 
either a clean flat `str` (for single lines) or a frozen `tuple[str, ...]` (for multi-line blocks).

## Operational Normalization Flow
1. **Direct String Passthrough**: If a raw `str` is provided, it is returned instantly. 
   This avoids wrapping single-line inputs into a redundant single-element tuple container.
2. **Collection Sanitization & Compaction**: If a `tuple` or `list` is provided, the engine 
   filters out non-string types, empty entries, or whitespace-only blocks.
3. **Smart Unboxing Optimization**: If a sanitized collection yields **exactly one** valid text element, 
   the engine unboxes it and returns it as a primitive `str`. If multiple elements are present, 
   it locks them inside an immutable `tuple[str, ...]`.
4. **Fallback Chain**: If the input is empty, invalid, `None`, or `UNSET`, the engine falls back 
   to the static class-level property default registered on `instance.__class__`.

## Performance Metrics and Memory Footprint
By mapping single-line text inputs to primitive `str` types instead of forcing object wrappers, 
the architecture harvests significant advantages:
- **Zero Object Allocation Overhead**: Eliminates thousands of short-lived tuple allocation 
  and garbage collection cycles during massive validation operations.
- **Fast-Path Layout Triggers**: Downstream rendering tiskárny (`print_problem`, etc.) can query 
  `isinstance(payload, str)` to fire ultra-fast string additions, completely bypassing loops, 
  slicing operations, or vertical margin padding computations.

## Public Typing Alignment
Even though `list[str]` is natively intercepted as a deliberate user convenience feature, 
it is omitted from the public facing type signatures to maintain explicit architectural bounds. 
The official structural boundary type contract remains:
```python
problem: tuple[str, ...] | str | None = None
context: tuple[str, ...] | str | None = None
how_to_fix: tuple[str, ...] | str | None = None

```

## Usage Scope

Invoked dynamically inside `SimpleException.__init__` during execution initialization:

```python
self.problem = normalize_strings(self, problem, "problem")
self.context = normalize_strings(self, context, "context")
self.how_to_fix = normalize_strings(self, how_to_fix, "how_to_fix")

```

"""