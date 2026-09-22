from .build_validation_error import build_validation_error


_DESIGN_NOTES = """
# Validation Errors Builders Sub-Package

## Purpose
Houses optional factory functions that assemble a structured `ValidationError`-family exception
instance ready to be raised by the caller. Builders never call `raise` themselves — they only return
the built exception — so the caller's own `raise` statement is what the location scanner sees,
keeping reported error locations accurate without needing offset tricks.

## Inclusion Rule
A builder is added **only** when it encapsulates logic beyond rearranging constructor arguments —
e.g. extracting a callable's `__name__`, deriving a dynamic `expected` string from a type, or similar
computed content. If a builder would just forward its parameters into the exception's constructor
under different names, it is not created; the caller raises the exception class directly instead.

## Registry

| Component                  | Type     | Description                                                                          |
| :--------------------------- | :------- | :------------------------------------------------------------------------------------ |
| `build_validation_error`   | Function | Builds a `ValidationError` for a failed user-supplied callable rule (lambda/function). |
"""