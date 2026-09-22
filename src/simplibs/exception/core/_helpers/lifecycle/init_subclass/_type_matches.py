from typing import Union, get_origin, get_args, Any
from types import UnionType


def _type_matches(
    value: object,
    typ: type
) -> bool:
    """
    Recursively checks whether a value matches a (possibly parameterized) type.

    Handles:
        - Any                          -> always matches
        - X | Y / Union[X, Y]          -> matches if any member matches
        - tuple[str, ...], list[X]...  -> checked only against the origin
                                           container (e.g. tuple), not the
                                           inner element types
        - plain types                  -> standard isinstance check
    """

    # 1. Any takes precedence — always matches, no further check needed
    if typ is Any:
        return True

    # 2. Handle parameterized types
    origin = get_origin(typ)
    if origin is not None:

        # 2.1 Recursively check a union type
        if origin is UnionType or origin is Union:
            return any(
                _type_matches(value, arg)
                for arg in get_args(typ)
            )

        # 2.2 Check a simple parameterized type against its origin container
        # noinspection PyTypeChecker
        return isinstance(value, origin)

    # 3. Handle a plain, non-parameterized type
    return isinstance(value, typ)


_DESIGN_NOTES = """
# type_matches

## Purpose
A recursive replacement for plain `isinstance()`, needed because `isinstance`
cannot handle two type shapes that are common in `SimpleExceptionData`'s
annotations:

    isinstance(val, str | UnsetType)   # TypeError-free, but doesn't recurse
                                        # into union members the way this
                                        # function's callers need
    isinstance(val, tuple[str, ...])   # TypeError: isinstance() argument 2
                                        # cannot be a parameterized generic

`type_matches` normalises both cases into a single, always-callable check —
used by `check_children_class_attributes` to validate subclass attribute
types against the schema declared in `SimpleExceptionData`.

## Processing flow

### Step 1 — Any
`Any` is the explicit escape hatch: if the parent annotation says `Any`,
no value could ever fail the check, so it returns `True` immediately without
inspecting `origin` at all.

### Step 2 — parameterized types (origin is not None)
`get_origin(typ)` returns `None` for plain types (`str`, `int`, custom
classes) and something non-`None` for parameterized ones — `types.UnionType`
for `X | Y`, `typing.Union` for `Union[X, Y]`, `tuple` for `tuple[str, ...]`,
`list` for `list[int]`, and so on.

#### Step 2.1 — unions
For `X | Y` (PEP 604) or `Union[X, Y]`, the function recurses into
`get_args(typ)` — the individual member types — and matches if *any* one of
them matches. This is what makes `str | UnsetType` actually validate `str`
**and** `UnsetType` correctly, instead of being skipped entirely (which is
what a naive `get_origin(typ) is None` guard used to do before this function
existed).

#### Step 2.2 — other parameterized generics
For anything else with a non-`None` origin (`tuple[str, ...]`, `list[int]`,
etc.), only the origin container is checked — `isinstance(value, tuple)`,
not "is every element inside a str?". This is a deliberate boundary, not an
oversight: validating element types would require another layer of recursion
(iterate the container, check each element, decide how to report a failure
at a given index) for marginal benefit, especially since fields like
`how_to_fix: tuple[str, ...]` already pass through their own
`_process_how_to_fix_param` normalisation at `__init__` time. This function
confirms *shape* (right container type), not *deep content*.

`# noinspection PyTypeChecker` suppresses a static-analysis warning on this
line — `origin` is typed as `type | None` from `get_origin`'s signature, but
step 2's `if origin is not None` already guarantees it's a concrete type by
the time `isinstance` is called. The type checker can't see that guarantee
because it only tracks types by declaration, not by the narrowing already
performed a few lines above.

### Step 3 — plain types
If `origin` is `None`, `typ` is a plain, non-parameterized type (`str`,
`int`, a custom class) — a direct `isinstance(value, typ)` is safe and
sufficient.

## Notes
- The function is pure and side-effect-free — same inputs always produce the
  same output, making it easy to reason about and safe to call repeatedly
  (e.g. once per attribute in `check_children_class_attributes`).
- Recursion depth is bounded by how deeply nested the annotation itself is —
  in practice, one level (a union of at most a couple of parameterized
  members) for every field currently defined on `SimpleExceptionData`.
"""