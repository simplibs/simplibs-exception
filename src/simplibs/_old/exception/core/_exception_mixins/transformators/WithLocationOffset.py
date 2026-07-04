from typing import Self


class WithLocationOffsetMixin:
    """Mixin providing the ability to create a new instance with a shifted stack depth."""

    def with_location_offset(
        self: Self,
        offset: int = 1
    ) -> Self:
        """
        Creates a new exception instance with increased get_location depth.

        Use this when you're re-raising an exception from a wrapper function
        and want to skip the wrapper to show the original caller.
        """
        # 1. Compute new depth (if get_location is an integer)
        new_get_location = (
            self._get_location + offset
            if self._get_location else self._get_location
        )

        # 2. Use the current class type (supports inheritance automatically)
        cls = type(self)

        # 3. Create a new instance with the same data but new location
        # Values are passed directly; if they are UNSET, they remain UNSET in the new instance.
        new_exc = cls(
            message=self.message,
            value=self.value,
            value_label=self.value_label,
            expected=self.expected,
            problem=self.problem,
            context=self.context,
            how_to_fix=self.how_to_fix,
            error_name=self.error_name,
            exception=self.exception,
            get_location=new_get_location,
            skip_locations=self._skip_locations,
            oneline=self._oneline,
        )

        # 4. Return new instance (the message is re-rendered with the new location)
        return new_exc


_DESIGN_NOTES = """
# WithLocationOffsetMixin

## Purpose
Allows "re-targeting" an existing exception. This is crucial for library 
authors who catch an error and want to re-raise it so that the user sees 
the line in *their* code where they called the library, not the line 
*inside* the library where the re-raise happened.

## Logic
It creates a completely new instance of the current class (`type(self)`). 
Because the new instance calls `__init__`, the `_render_message()` is 
triggered again, correctly picking up the location at the new stack depth.

## Clean Code Improvements
- **Self-reference:** Uses `type(self)` and `typing.Self` to avoid 
  circular imports and support subclasses.
- **Direct Assignment:** Parameters are passed directly to the constructor 
  without redundant `is not UNSET` checks. If a value is `UNSET`, it is 
  simply passed as `UNSET`, which is the desired behavior.
- **Decoupling:** Removed explicit attribute type declarations and 
  `TYPE_CHECKING` blocks to keep the mixin lightweight.
"""