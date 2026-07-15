# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2026-07-16

### ⚠️ Breaking Changes

* **Renamed Property**: `value_label` in `SimpleExceptionData` (and `SimpleException`) has been renamed to `label`. This provides broader context usage for exceptions even when no `value` is present.
* **Dependency Constraint**: Recommend using `~= 0.2.0` in dependent projects to avoid automatic upgrades to 1.0.0 due to breaking changes.

### 🔄 Changed

* **Code Refactoring**: Massive transition from Mixin-based logic to functional composition within `_core_logic`. This significantly lightens the class MRO and improves maintainability.
* **Internal Structure**: All supporting logic (previously mixin methods) has been moved to internal-only functional utilities within `_core_logic`, ensuring clean separation between internal mechanics and public API.

### ✨ Added

* **Testing Ecosystem**: Introduced a comprehensive `testing` package containing advanced tools (such as `assert_exception_class`, custom assertions, and automated bulk test matrix engines) to easily validate exceptions, custom subclasses, and functional logic.
* **Multi-line Support**: `problem` and `context` fields now support `tuple[str, ...]` input, allowing for structured multi-line output in all modes.

### 📋 Improved

* **Stability**: Refactored the core engine for production readiness; transitioned to version 1.0.0 to signal API stability.
* **Codebase Cleanliness**: Removed redundant mixin boilerplate in favor of specialized initialization and normalization functions.

---

## [0.2.0] - 2026-04-11

### 🔄 Changed

* **Core Architecture**: Unified rendering workflow by centralizing logic into the data layer (`SimpleExceptionData`)
* **Output Modes API**: All output modes (`PRETTY`, `SIMPLE`, `LOG`, `ONELINE`) now accept only `data: SimpleExceptionData` parameter
* **Location Resolution**: Decoupled manual `caller_info` dictionary passing; call stack introspection now handled lazily via `SimpleExceptionData.caller_info`
* **Mixin Composition**: Refactored `ModeBase` to use explicit mixin hierarchy (`RenderMessageMixin`, `PrintCallerInfoMixin`, `PrintIntroLineMixin`, `PrintValueWithTypeMixin`)
* **Internal Structure**: Reorganized core modules:
* Separated workflow logic into dedicated mixins for better separation of concerns
* Created `_data_mixin` layer for data-centric operations
* Improved code reusability across the ecosystem



### ✨ Added

* **New Tools in `tools/**`:
* `raise_with_location_offset()`: Function for raising exceptions with custom stack depth adjustment
* `raise_location_offset`: Decorator for elegant stack offset handling in helper functions
* `decorators/` subpackage for composable decorator utilities


* **Smart Value Truncation**: Advanced truncation in `PrintValueWithTypeMixin` with character count indication
* **Enhanced Data Layer**: `SimpleExceptionData` now includes lazy-loaded `caller_info` property
* **New Setting**: `DEFAULT_VALUE_TRUNCATION_LENGTH` for controlling max value display length

### 🐛 Fixed

* **Consistency**: Standardized all helper method signatures across mixins
* **Documentation**: Updated all Design Notes to reflect current architecture (removed historical notes)
* **Import Structure**: Clarified lazy import patterns to prevent circular dependencies
* **Type Hints**: Enhanced type annotations across the codebase

### 📋 Improved

* **Code Organization**: Flattened public API while maintaining deep modularity internally
* **Testability**: Each mixin is now independently testable
* **Readability**: Design notes in each module now match actual implementation exactly

---

## [0.1.1] - 2026-03-30

### 🐛 Fixed

* **README**: Corrected outdated import paths and library references
* **Documentation**: Updated example code snippets to match current package structure
* **Type Hints**: Fixed incomplete type annotations in utility functions

---

## [0.1.0] - 2026-03-30

### ✨ Added

#### Core Exception Class

* `SimpleException` — structured exception with diagnostic output and rich formatting

#### Parameters & Customization

* Support for `message`, `value`, `value_label`, `expected`, `problem`, `context`, `how_to_fix`
* Support for `error_name`, `exception`, `get_location`, `skip_locations`, `oneline`
* Custom exception subclasses with inherited defaults
* Runtime validation of subclass attributes

#### Output Modes

* `PRETTY` — framed structured output (default)
* `SIMPLE` — plain text without decorative lines
* `ONELINE` — compact single-line format
* `LOG` — machine-readable key=value format
* `ModeBase` — abstract base for custom modes

#### Configuration & Settings

* `SimpleExceptionSettings` — global configuration for the entire ecosystem
* Settings validation with clear error messages
* Support for mode switching and location reporting control

#### Serialisation

* `to_dict()` — public attributes as dictionary
* `to_json()` — JSON string representation
* `to_debug_dict()` — complete internal state for debugging

#### Developer Tools

* `bool_or_exception()` — boolean result to exception conversion
* `extract_caller_info()` — independent call stack introspection
* Location tracking and stack depth control

#### Quality Assurance

* Full test coverage (~281 tests)
* Unit and integration tests
* Living documentation via test examples

#### Dependencies

* `simplibs-sentinels` — sentinel values (`UNSET`) for distinguishing unset from `None`

---

## Legend

* 🔄 **Changed** — modifications to existing functionality
* ✨ **Added** — new features and components
* 🐛 **Fixed** — bug fixes
* 📋 **Improved** — enhancements to existing features
* ⚠️ **Deprecated** — deprecated functionality (not used yet in this project)
* 🗑️ **Removed** — removed functionality (not used yet in this project)