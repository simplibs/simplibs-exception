from .base_error.SimpleError import SimpleError
from .validations_errors.ValidationError import ValidationError
from .validations_errors.ParamError import ParamError
from .state_errors.StateError import StateError
from .state_errors.InitializationError import InitializationError
from .state_errors.ConfigurationError import ConfigurationError
from .resource_errors.ResourceError import ResourceError
from .resource_errors.NotFoundError import NotFoundError
from .resource_errors.AlreadyExistsError import AlreadyExistsError
from .resource_errors.AccessError import AccessError
from .operation_errors.OperationError import OperationError
from .conversion_errors.ConversionError import ConversionError
from .dependency_errors.DependencyError import DependencyError


__all__ = [
    "SimpleError",
    "ValidationError",
    "ParamError",
    "StateError",
    "InitializationError",
    "ConfigurationError",
    "ResourceError",
    "NotFoundError",
    "AlreadyExistsError",
    "AccessError",
    "OperationError",
    "ConversionError",
    "DependencyError",
]


_DESIGN_NOTES = """
# Exceptions Public Package

## Purpose
Central, importable collection of every named, categorized exception in the `simplibs.exception`
ecosystem. Every simplibs library that needs a general-purpose exception (parameter validation,
state, resource, ...) imports it from here instead of redefining an equivalent one locally.

## Public API Export Strategy

* **Top-Level Re-exports:**
  Re-exports all standard, non-domain exception classes (`SimpleError`, `ValidationError`,
  `ParamError`, `StateError`, `InitializationError`, `ConfigurationError`, `ResourceError`,
  `NotFoundError`, `AlreadyExistsError`, `AccessError`, `OperationError`, `ConversionError`,
  `DependencyError`) directly at the package root level.
* **Single Source of Import:**
  Consumers and internal packages can import all common exception types directly from
  `simplibs.exception` (e.g. `from simplibs.exception import ValidationError, ParamError`)
  without needing to navigate internal directory structures or sub-modules like
  `simplibs.exception.validations_errors.ValidationError`.
* **Explicit Exclusions:**
  Builders/factories (e.g. from sub-packages' `builders` modules) are deliberately excluded
  from top-level re-exports to keep the main namespace clean and focused exclusively on exception types.
  
## Consolidated Architecture Mapping

| Category                    | Description                                                                          |
| :--------------------------- | :------------------------------------------------------------------------------------ |
| **Core Exception**          | Structural root of the categorized tree (`SimpleError`).                             |
| **Validation Errors**       | Exceptions for values/parameters that fail to satisfy a required condition.          |
| **State Errors**            | Exceptions for objects/systems not in the state an operation requires.               |
| **Resource Errors**         | Exceptions for problems working with identifiable resources.                         |
| **Operation Errors**        | Exceptions for runtime operations/processes that failed while executing.             |
| **Conversion Errors**       | Exceptions for values that could not be converted between types/formats.             |
| **Dependency Errors**       | Exceptions for missing, incompatible, or unavailable dependencies.                   |
| **Builders**                | Optional factory functions for exceptions whose message needs computed content; not re-exported here — import explicitly from the relevant sub-package's `builders`. |

## Registry

| Component              | Type  | Description                                                                 |
| :------------------------ | :---- | :---------------------------------------------------------------------------- |
| `SimpleError`           | Class | Root of all named, categorized exceptions. Never raised directly.            |
| `ValidationError`       | Class | A value or input failed to satisfy a required condition.                     |
| `ParamError`            | Class | A function or constructor parameter failed validation.                       |
| `StateError`            | Class | An object or system is not in the state a given operation requires.         |
| `InitializationError`   | Class | An object or system was used before it was properly initialized.            |
| `ConfigurationError`    | Class | Required configuration is missing or invalid.                               |
| `ResourceError`         | Class | A problem occurred while working with an identifiable resource.             |
| `NotFoundError`         | Class | A requested resource does not exist.                                        |
| `AlreadyExistsError`    | Class | A resource could not be created because it already exists.                  |
| `AccessError`           | Class | A resource exists but cannot be accessed due to missing permissions or a lock. |
| `OperationError`        | Class | A runtime operation or process failed while executing.                      |
| `ConversionError`       | Class | A value could not be converted from one type or format to another.          |
| `DependencyError`       | Class | A required dependency is missing, incompatible, or failed to load.          |
"""