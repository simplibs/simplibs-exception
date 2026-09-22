from .DependencyError import DependencyError


_DESIGN_NOTES = """
# Dependency Errors Sub-Package

## Purpose
Groups exceptions concerned with "a required dependency is missing, incompatible, or failed to load".

## Registry

| Component          | Type  | Description                                                          |
| :-------------------- | :---- | :---------------------------------------------------------------------- |
| `DependencyError`  | Class | A required dependency is missing, incompatible, or failed to load.  |
"""