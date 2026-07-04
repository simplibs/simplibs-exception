from .dunders import DunderInitSubclassMixin, DunderNewMixin
from .transformators import WithLocationOffsetMixin
from .normalizers import (
    NormalizeParamMixin,
    ProcessExceptionParamMixin,
    ProcessGetLocationParamMixin,
    ProcessHowToFixParamMixin,
    ProcessSkipLocationsParamMixin
)
from .serializers import (
    ToDictMixin,
    ToDebugDictMixin,
    ToJsonMixin
)


_DESIGN_NOTES = """
# _exception_mixins

## Purpose
The central entry point for all functional mixins used by `SimpleException`. It 
aggregates behavior from specialized sub-packages and exposes them through a 
flat interface for the main exception class.

## Contents
The mixins are categorized into logical groups:

| Group            | Responsibility                                               |
|------------------|--------------------------------------------------------------|
| `dunders`        | Class lifecycle and dynamic MRO management                   |
| `normalizers`    | Sanitization and validation of input parameters              |
| `transformators` | Methods for creating modified instances (e.g., location shift)|
| `serializers`    | Data export formats (dict, json, debug)                      |

## Design Rule: Encapsulation
Internal implementation details (utilities) are hidden. Only the mixin classes 
themselves are exposed to keep the public API focused.

## Usage
This module allows the main `SimpleException` class to import all its 
building blocks from a single location, keeping its import block clean.
"""