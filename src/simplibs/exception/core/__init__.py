from .data import SimpleExceptionData
from ._internal_exception import SimpleExceptionInternalError


_DESIGN_NOTES = """
# core

## Contents
The data layer of the library — defines the exception structure and the base
internal exception that consumes this structure.

| Name                           | Description                                               |
|--------------------------------|-----------------------------------------------------------|
| `SimpleExceptionData`          | Data class — exception structure and default values       |
| `SimpleExceptionInternalError` | Base internal exception — foundation for grouped exceptions|

## Note
This package has no dependencies on the rest of the library — it is completely
isolated. Everything else draws from it; nothing points back into it.
"""