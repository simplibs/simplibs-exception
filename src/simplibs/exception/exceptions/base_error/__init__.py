from .SimpleError import SimpleError


_DESIGN_NOTES = """
# Core Exception Sub-Package

## Purpose
Houses the structural root of the categorized exception tree, kept separate from the rest of
`exceptions/` because it is a framework-internal anchor point rather than a domain-specific error
category — nothing outside this package should ever need to reach into it directly.

## Registry

| Component     | Type  | Description                                                                          |
| :------------- | :---- | :------------------------------------------------------------------------------------ |
| `SimpleError`  | Class | Root of all named, categorized exceptions. Never raised directly; never carries logic. |
"""