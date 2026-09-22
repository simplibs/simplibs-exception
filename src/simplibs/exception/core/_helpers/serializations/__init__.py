from .to_debug_dict import to_debug_dict
from .to_dict import to_dict


_DESIGN_NOTES = """
# Object State Serialization Sub-Package

## Purpose
Exposes internal state transformation routines that convert frozen exception data containers into 
primitive Python dictionary layouts suitable for debugging, testing, or machine-readable logging.

## Internal Components Registry

| Component       | Type     | Description                                                                     |
| :-------------- | :------- | :------------------------------------------------------------------------------ |
| `to_dict`       | Function | Exports the essential exception state into a standard dictionary.               |
| `to_debug_dict` | Function | Exports the complete internal state for debugging and diagnostics.              |
"""