from .Kwargs import Kwargs
from .TestCase import TestCase

__all__ = [
    "Kwargs",
    "TestCase",
]

_DESIGN_NOTES = """
# Testing Data Containers High-Level Registry

## Purpose
Acts as the primary public interface for the testing framework's data encapsulation layer. 
It exposes structural blueprints used by developers to cleanly isolate operational payloads 
and declare comprehensive test case execution matrices.

## Universal Components Registry

| Component  | Type            | Description                                                                    |
| :--------- | :-------------- | :----------------------------------------------------------------------------- |
| `Kwargs`   | Data Container  | Wraps keyword arguments to prevent collisions during dynamic execution.        |
| `TestCase` | Test Definition | Encapsulates a complete test scenario with inputs, expectations, and metadata. |
"""