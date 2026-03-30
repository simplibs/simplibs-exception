from .SimpleExceptionInternalError import SimpleExceptionInternalError


_DESIGN_NOTES = """
# core/_internal_exception

## Contents
The base internal exception of the library — placed here because it inherits
directly from `SimpleExceptionData` and is therefore a natural part of the
data layer. Serves as the foundation for all grouped internal exceptions
in the library.

| Name                           | Description                                           |
|--------------------------------|-------------------------------------------------------|
| `SimpleExceptionInternalError` | Base internal exception — foundation for other groups |
"""