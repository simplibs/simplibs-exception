from .ResourceError import ResourceError
from .NotFoundError import NotFoundError
from .AlreadyExistsError import AlreadyExistsError
from .AccessError import AccessError


_DESIGN_NOTES = """
# Resource Errors Sub-Package

## Purpose
Groups every exception concerned with "a problem occurred while working with an identifiable
resource": the general `ResourceError` and its more specific descendants.

## Registry

| Component            | Type  | Description                                                                 |
| :---------------------- | :---- | :---------------------------------------------------------------------------- |
| `ResourceError`      | Class | A problem occurred while working with an identifiable resource.             |
| `NotFoundError`      | Class | A requested resource does not exist.                                        |
| `AlreadyExistsError` | Class | A resource could not be created because it already exists.                  |
| `AccessError`        | Class | A resource exists but cannot be accessed due to missing permissions or a lock. |
"""