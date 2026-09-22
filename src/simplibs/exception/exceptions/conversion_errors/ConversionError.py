# Inners
from ..base_error.SimpleError import SimpleError


class ConversionError(SimpleError):
    """A value could not be converted from one type or format to another.

    General-purpose exception for failed conversions/casts/parses —
    distinct from `ValidationError`, since the input may be well-formed but
    simply incompatible with the target type or format.
    """
    pass


_DESIGN_NOTES = """
# ConversionError

## Purpose
General-purpose exception for "a value could not be converted from one type or format to another"
(e.g. string-to-number parsing, serialization/deserialization, type casting between simplibs objects).

## Rationale
Kept distinct from `ValidationError`: validation asks "does this value satisfy a rule", conversion
asks "can this value be transformed into a different representation". A value can be perfectly valid
in its own type and still fail to convert (e.g. an int too large for a target fixed-width type).
"""