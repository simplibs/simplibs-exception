from typing import TYPE_CHECKING, Any, NoReturn
# Annotations
if TYPE_CHECKING:
    from ..protocols import SimpleExceptionProtocol


def raise_with_location_offset(
    exc: "BaseException | SimpleExceptionProtocol | Any",
    offset: int = 1,
) -> NoReturn:
    """Takes an exception, applies a relative stack-frame location offset if supported, and raises it.

    Acts as an operational functional wrapper shortcut for the fluent method call:
    `raise exc.with_location_offset(offset)`

    Args:
        exc: The target exception instance to be processed and thrown.
        offset: The relative number of frames to shift the location tracing vector back.

    Raises:
        BaseException: The incoming exception instance, with or without a mutated trace context.
    """
    # 1. Evaluate via runtime duck-typing whether the exception supports frame shifting mutation
    if hasattr(exc, "with_location_offset"):
        raise exc.with_location_offset(offset)

    # 2. Resilient fallback for standard Python exceptions (e.g. ValueError, TypeError).
    # Using 'from None' prevents Python from compounding a local frame mutation exception context,
    # thereby fully preserving the original underlying traceback of the raw exception object.
    raise exc from None


_DESIGN_NOTES = """
# raise_with_location_offset

## Purpose
A specialized operational wrapper optimized for advanced error-propagation and re-targeting tasks. 
It enables developers to cleanly recalibrate and trigger an exception's internal stack trace tracking 
state in a single unified command pass.

## Code Pattern Comparison

### Standard Blueprint Context
```python
try:
    process_data(payload)
except ValueError as err:
    exc = SimpleException("Processing failed", exception=err)
    raise exc.with_location_offset(1)

```

### Consolidated Utility Layout

```python
try:
    process_data(payload)
except ValueError as err:
    raise_with_location_offset(SimpleException("Processing failed", exception=err), 1)

```

## Architectural Duck-Typing Constraints

To completely dismantle import-time dependency loops and remain decoupled from specific high-level exception
blueprints, the function relies on explicit structural duck-typing. It validates the presence of the
`with_location_offset` method programmatically at runtime.

## Standard Python Fallback Interception

When consuming native standard exceptions (such as `KeyError`), the target object lacks the custom trace-shifting
API. The system seamlessly downgrades into a generic passthrough dispatcher. Triggering `raise exc from None`
ensures that the core interpreter contextually emits the existing object matrix while isolating the
original traceback graph from being overwritten by this helper tool's local frame.
"""
