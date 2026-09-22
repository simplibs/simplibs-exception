from .ValidationError import ValidationError
from .ParamError import ParamError


_DESIGN_NOTES = """
# Validation Errors Sub-Package

## Purpose
Groups every exception concerned with "a value or input failed to satisfy a required condition":
the general `ValidationError` and its more specific `ParamError`. Optional message-building helpers
for this family live separately in `builders/` and are not re-exported here.

## Registry

| Component         | Type  | Description                                                                 |
| :------------------- | :---- | :---------------------------------------------------------------------------- |
| `ValidationError`  | Class | A value or input failed to satisfy a required condition.                     |
| `ParamError`       | Class | A function or constructor parameter failed validation.                       |
"""