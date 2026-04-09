# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog,
and this project adheres to Semantic Versioning.


## [0.1.1] - 2026-03-30

### Fixed
- README: Corrected outdated import paths and library references.
- Documentation: Fixed example code snippets to align with the current package structure.


## [0.1.0] - 2026-03-30

### Added
- `SimpleException` — structured exception with diagnostic output
- Support for `message`, `value`, `value_label`, `expected`, `problem`,
  `context`, `how_to_fix`, `error_name`, `exception`, `get_location`,
  `skip_locations`, and `oneline` parameters
- Four output modes: `PRETTY`, `SIMPLE`, `ONELINE`, `LOG`
- `SimpleExceptionSettings` — global configuration for the entire ecosystem
- Custom mode support via `ModeBase`
- Serialisation via `to_dict()`, `to_json()`, `to_debug_dict()`
- Utility tools: `bool_or_exception`, `extract_caller_info`
- Sentinel values via `simplibs-sentinels` dependency
- Full test coverage (~281 tests)