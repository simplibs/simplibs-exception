# Dunders
from .dunders import DunderInitSubclassMixin, DunderNewMixin
# Normalizers
from .normalizers import (
    NormalizeParamMixin,
    ProcessExceptionParamMixin,
    ProcessHowToFixParamMixin,
    ProcessGetLocationParamMixin,
    ProcessSkipLocationsParamMixin,
)
# Serializers
from .serializers import ToDictMixin, ToDebugDictMixin, ToJsonMixin


_DESIGN_NOTES = """
# exception/_mixins

## Contents
The aggregation point for all mixins of the `SimpleException` class.
Imports from subpackages and re-exports them as a unified interface.

| Package       | Mixins                                                                 |
|---------------|------------------------------------------------------------------------|
| `dunders`     | DunderInitSubclassMixin, DunderNewMixin                                |
| `normalizers` | NormalizeParamMixin, ProcessExceptionParamMixin,                       |
|               | ProcessHowToFixParamMixin, ProcessGetLocationParamMixin,               |
|               | ProcessSkipLocationsParamMixin                                         |
| `serializers` | ToDictMixin, ToDebugDictMixin, ToJsonMixin                             |

## Usage
    from ._mixins import (
        DunderInitSubclassMixin,
        DunderNewMixin,
        NormalizeParamMixin,
        ProcessExceptionParamMixin,
        ProcessHowToFixParamMixin,
        ProcessGetLocationParamMixin,
        ProcessSkipLocationsParamMixin,
        ToDictMixin,
        ToDebugDictMixin,
        ToJsonMixin,
    )
"""