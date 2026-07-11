from .exceptions_bulk_test import exceptions_bulk_test
from .FunctionCase import FunctionCase

__all__ = [
    "exceptions_bulk_test",
    "FunctionCase",
]

_DESIGN_NOTES = """
# Bulk Test Sub-Engine Registry

## Purpose
Provides the primary interface for automated bulk verification of exception boundaries. 
This module consolidates the orchestration logic required to process heterogeneous collections 
of testing targets (classes, functions, and scenarios) through a unified matrix runner.

## Component Registry

| Component             | Type                 | Description                                              |
| :-------------------- | :------------------- | :------------------------------------------------------- |
| `exceptions_bulk_test`| Master Orchestrator  | The entry point for executing bulk validation pipelines. |
| `FunctionCase`        | Declarative Schema   | Container for defining isolated functional test scenarios.|

## Usage Pattern
This module is designed to be imported at the test suite level. It is the recommended 
way to instantiate and run comprehensive multi-target audit matrices, ensuring 
consistent telemetry and reporting across the entire library.
"""