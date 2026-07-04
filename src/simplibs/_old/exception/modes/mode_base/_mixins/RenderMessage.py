from typing import Self
from simplibs.sentinels import UNSET
# Outers
from ....core import SimpleExceptionData


# noinspection PyProtectedMember
class RenderMessageMixin:
    """Mixin for message rendering workflow — handles the logic of building exception output."""

    def render_message(
        self: Self,
        data: SimpleExceptionData,
        *,
        validate: bool = True
    ) -> str:
        """
        Selects the appropriate output based on the data content and returns the assembled string.

        Args:
            data:     Exception data conforming to SimpleExceptionData.
            validate: If True, verifies that the data matches the expected protocol.

        Returns:
            The assembled exception output string.
        """
        # 1. Optional data validation
        if validate:
            from .validations import validate_has_simple_exception_data
            validate_has_simple_exception_data(data)

        # 2. Detect whether content fields are present for a full output
        has_base_content = not (
            data.value is UNSET
            and data.expected is UNSET
            and data.problem is UNSET
            and data.context is UNSET
            and data.how_to_fix is UNSET
        )

        # 3. Select the appropriate output based on data content
        if not has_base_content:
            if data.message is UNSET:
                return self._empty_outcome(data)
            return self._message_outcome(data)

        return self._full_outcome(data)


_DESIGN_NOTES = """
# RenderMessageMixin

## Purpose
Encapsulates the message rendering workflow. Its sole responsibility is to 
analyze the state of `SimpleExceptionData` and delegate the actual string 
assembly to the appropriate "outcome" method.

## Major Change: Decoupled Location Logic
The location logic has been moved to the data layer (`SimpleExceptionData`). 
`RenderMessageMixin` no longer handles stack introspection, making it 
completely decoupled from stack depth calculations.

## The render_message workflow

### Step 1: Optional validation
Verifies that the input follows the `SimpleExceptionData` protocol. 
Validation is performed lazily to avoid circular imports.

### Step 2: Scenario detection
Determines if the exception contains "structured" content (`value`, `expected`, 
`problem`, etc.) or if it should fallback to a simple `message`.

### Step 3: Output method selection
Delegates to the specific outcome methods defined in `ModeBase`. 

| Scenario      | Condition                                              | Method           |
|---------------|--------------------------------------------------------|------------------|
| Empty call    | No content fields and no message provided              | _empty_outcome   |
| Message only  | Message provided, no content fields present            | _message_outcome |
| Full output   | At least one content field is present                  | _full_outcome    |

## Integration
This mixin acts as the "brain" of a Mode. While `ModeBase` defines what can 
be printed (the interface), `RenderMessageMixin` defines the logic of 
when to print what (the workflow). 

Note: The `__call__` method is implemented in the `ModeBase` class to 
provide a clear entry point for making mode instances callable.
"""