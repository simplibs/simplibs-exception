from .maybe_subtest import maybe_subtest


_DESIGN_NOTES = """
# Testing Common Utilities Sub-Package

## Purpose
Houses shared cross-functional lifecycle primitives and context proxies utilized across both 
individual assertions and bulk automated test executors.

## Internal Components Registry

| Component       | Type            | Description                                                                  |
| :-------------- | :-------------- | :--------------------------------------------------------------------------- |
| `maybe_subtest` | Context Manager | Conditionally wraps execution in a subtest context when supported or needed. |
"""