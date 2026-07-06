from typing import TYPE_CHECKING
# Annotations
if TYPE_CHECKING:
    from ...protocols import SimpleExceptionProtocol


def with_location_offset(
    instance: "SimpleExceptionProtocol",
    offset: int = 1
) -> "SimpleExceptionProtocol":
    """
    Creates a new exception instance with increased get_location depth.

    Use this when you're re-raising an exception from a wrapper function
    and want to skip the wrapper to show the original caller.
    """
    # 1. Compute new depth safely handling both integer offsets and boolean triggers
    if isinstance(instance.get_location, bool):
        # If True (1), adds offset (e.g., 1 + 1 = 2). If False, remains False.
        new_get_location = (
            (instance.get_location + offset) if instance.get_location else False
        )
    else:
        # If it's already a specific integer depth, just advance it forward
        new_get_location = instance.get_location + offset

    # 2. Use the current class type (supports dynamic MRO inheritance automatically)
    cls = type(instance)

    # 3. Create a new instance with the identical payload data but an advanced location target
    new_exc = cls(
        message=instance.message,
        value=instance.value,
        label=instance.label,
        expected=instance.expected,
        problem=instance.problem,
        context=instance.context,
        how_to_fix=instance.how_to_fix,
        error_name=instance.error_name,
        exception=instance.exception,
        get_location=new_get_location,
        skip_locations=instance.skip_locations,
        oneline=instance.oneline,
    )

    # 4. Return new instance (the internal core will re-render the message at the new frame depth)
    return new_exc


_DESIGN_NOTES = """
# with_location_offset

## Purpose
Allows "re-targeting" or shifting the stack frame location context of an existing exception. 
This is a critical framework feature for library authors who catch an internal error and want to 
re-raise it so that the end-user sees the exact line in *their own application code* where they 
invoked the library, completely bypassing the internal wrapper function frames.

## Mechanical Execution Lifecycle
Instead of modifying the state of an active exception in-place (which would corrupt the message cache 
and break immutability contracts), the function spawns a completely fresh instance via `type(instance)`. 
As this new object passes through the standard `__init__` constructor lifecycle, the framework's 
internal stack scanner is triggered again, successfully capturing the caller metadata at the newly 
calibrated stack frame depth.

## Defensive Depth Computation Logic
The input field `get_location` supports a hybrid type interface (`int | bool`). The calculation logic 
safely prevents type-coercion pitfalls:
- **Boolean True (Active Default)**: Interpreted as baseline depth `1`. Adding an offset of `1` smoothly 
  advances the depth state to integer `2`, pushing the frame lookup pass past the intercepting wrapper.
- **Boolean False (Deactivated)**: If frame location tracing was explicitly disabled on the original 
  exception, it remains firmly `False`. An offset modification cannot forcefully activate tracing.
- **Integer Depth**: If the exception is already utilizing a specific fixed frame offset layer, the engine 
  performs standard arithmetic addition to shift the frame scan window deeper into the runtime stack.

## Decoupled Architecture Benefice
By transitioning this logic from a traditional class Mixin method into a decoupled standalone utility 
function operating on a clean `instance` parameter:
- **Zero Circular MRO Loops**: Shifting logic out of the core exception base inheritance tree prevents 
  complex multi-inheritance dependency hell.
- **Payload Pass-through**: State attributes are mapped transparently. `UNSET` tokens pass cleanly 
  into the new constructor without requiring verbose filter maps, perfectly preserving variable boundaries.
"""