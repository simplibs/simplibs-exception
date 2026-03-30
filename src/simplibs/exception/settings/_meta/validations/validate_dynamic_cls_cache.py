# Inners
from .SimpleExceptionSettingsError import SimpleExceptionSettingsError


def validate_dynamic_cls_cache(value):
    """Verifies that the value is an empty dict — only allowed for cache reset."""
    if value != {}:
        raise SimpleExceptionSettingsError(
            value       = value,
            value_label = "_dynamic_cls_cache",
            expected    = "an empty dict {} — for cache reset only",
            problem     = "the cache is not intended to be overwritten manually",
            how_to_fix  = (
                "To reset the cache use: SimpleExceptionSettings.reset()",
                "To reset manually assign an empty dict: SimpleExceptionSettings._dynamic_cls_cache = {}",
            ),
        )


_DESIGN_NOTES = """
# validate_dynamic_cls_cache

## Purpose
Validates writes to `_dynamic_cls_cache` in `SimpleExceptionSettings`.
This attribute is not intended for manual assignment — the only permitted
value is an empty dict `{}`, which serves as a cache reset.

## Why an empty dict is permitted
The cache is populated exclusively and automatically by `DunderNewMixin.__new__`
at runtime. A manual reset to `{}` is the only legitimate intervention —
it clears all cached dynamic classes, for example during testing or dynamic
module reloading.
"""