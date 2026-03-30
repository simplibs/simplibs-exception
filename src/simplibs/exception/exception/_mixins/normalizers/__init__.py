from .NormalizeParam import NormalizeParamMixin
from .ProcessHowToFixParam import ProcessHowToFixParamMixin
from .ProcessExceptionParam import ProcessExceptionParamMixin
from .ProcessGetLocationParam import ProcessGetLocationParamMixin
from .ProcessSkipLocationsParam import ProcessSkipLocationsParamMixin


_DESIGN_NOTES = """
# exception/_mixins/normalizers

## Contents
Mixins for normalising the input parameters of `SimpleException.__init__`.
None of them raise an exception — unsuitable inputs are silently replaced
with the class-level default or a value from settings.

| Name                            | Method                          | Description                                          |
|---------------------------------|---------------------------------|------------------------------------------------------|
| `NormalizeParamMixin`           | `_normalize_param`              | Normalises simple types (str, int, bool)             |
| `ProcessExceptionParamMixin`    | `_process_exception_param`      | Processes the exception parameter — class or instance|
| `ProcessHowToFixParamMixin`     | `_process_how_to_fix_param`     | Normalises str or tuple to tuple[str, ...]           |
| `ProcessGetLocationParamMixin`  | `_process_get_location_param`   | Processes get_location — falls back to settings      |
| `ProcessSkipLocationsParamMixin`| `_process_skip_locations_param` | Normalises skip_locations and merges with blacklist  |
"""