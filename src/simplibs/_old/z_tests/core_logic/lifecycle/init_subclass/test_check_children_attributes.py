# Outers
from ...internal_exceptions import SimpleExceptionInternalError
# Inners
from ._type_matches import _type_matches


def check_children_attributes(
    parent_class: type,
    child_class: type
) -> None:
    """
    Verifies that a subclass contains no unknown attributes and that their types
    match those declared in the parent class.

    Args:
        parent_class: The parent class whose annotations serve as the source of truth.
        child_class:  The subclass being validated.

    Raises:
        SimpleExceptionInternalError: If the subclass contains unknown attributes
                                       or attributes with incorrect types.
    """
    # 1. Parent annotations — public only, serve as the source of truth for both checks
    parent_annotations = {
        name: typ
        for name, typ in parent_class.__annotations__.items()
        if not name.startswith("_")
    }

    # 2. Subclass attributes — public only
    child_values = {
        name: getattr(child_class, name)
        for name in child_class.__dict__
        if not name.startswith("_")
    }

    # 3. Check for unknown attributes
    extra_keys = [k for k in child_values if k not in parent_annotations]
    if extra_keys:
        unused_keys = [k for k in parent_annotations if k not in child_values]
        raise SimpleExceptionInternalError(
            value=extra_keys,
            label=f"class '{child_class.__name__}'",
            expected=f"only attributes defined in '{parent_class.__name__}': {list(parent_annotations)}",
            problem="class contains unknown attributes — likely a typo",
            context=f"parent attributes not defined in subclass: {unused_keys}" if unused_keys else "",
            how_to_fix=(
                "Check for typos in the attribute names.",
                f"Permitted attributes are: {list(parent_annotations)}",
            ),
        )

    # 4. Type check
    type_errors = {
        name: {
            "value": val,
            "value_type": type(val).__name__,
            "expected_type": typ.__name__ if hasattr(typ, "__name__") else str(typ),
        }
        for name, val in child_values.items()
        if not _type_matches(val, (typ := parent_annotations[name]))
    }

    if type_errors:
        first_name, first_error = next(iter(type_errors.items()))
        raise SimpleExceptionInternalError(
            value=first_error["value"],
            label=f"'{first_name}' in class '{child_class.__name__}'",
            expected=first_error["expected_type"],
            problem=f"attribute has incorrect type — {len(type_errors)} error(s) found: {list(type_errors)}",
            how_to_fix=(
                f"Fix the type of attribute '{first_name}' to '{first_error['expected_type']}'.",
                "All attributes with type errors are listed in 'problem'.",
            ),
        )


_DESIGN_NOTES = """
# check_children_class_attributes

## Purpose
Validates a data class subclass at definition time — verifies that it contains
no unknown attributes and that their types match those declared in the parent.
Called from `SimpleException.__init_subclass__`.

## Why both checks live in one function
Steps 1 and 2 — retrieving parent annotations and subclass attributes — are
shared input data for both checks (steps 3 and 4). Splitting them would require
either duplicating these steps or passing the data as parameters, at which point
the functions would no longer be self-contained. One function with four numbered
steps is the cleaner and more natural solution here.

## Processing flow

### Step 1 — parent annotations
The source of truth for the entire validation. Only public annotations
(without a leading underscore) are loaded from `parent_class.__annotations__`.
In practice this is always `SimpleExceptionData` — the dedicated data-schema
class — never `SimpleException` itself, which now also carries behaviour and
would be a moving, unsuitable reference.

### Step 2 — subclass attributes
Only public attributes defined directly in `child_class.__dict__` are loaded —
that is, only those the subclass itself defines, not inherited ones.

### Step 3 — unknown attribute check
If the subclass contains an attribute that is not in the parent's annotations,
it is likely a typo. The exception includes:
- the list of unknown attributes
- the list of parent attributes not defined in the subclass (typo hint)
- the list of all permitted attributes

### Step 4 — type check
Verifies that the values of the subclass attributes match the types declared
in the parent, via `type_matches`. Unlike a plain `isinstance()` check, this
correctly handles:
- unions (`str | UnsetType`) — matches if any member of the union matches
- parameterized generics (`tuple[str, ...]`) — checked against their origin
  container only (e.g. `tuple`), not their inner element types
- `Any` — always matches, an explicit "unconstrained" escape hatch

See `type_matches`'s own design notes for the full breakdown of that logic;
this function only consumes it as a single boolean predicate per attribute.

## Behaviour on failure
The function raises `SimpleExceptionInternalError` — an internal library
exception that never surfaces as a user-facing error. This is a developer
error (incorrect class definition), not a runtime error.

## Notes
- The function is called at **class definition time**, not at instance
  creation — errors are therefore surfaced immediately on import, not on use.
- The walrus operator `:=` in step 4 captures the type directly inside the
  dict comprehension condition without needing a nested function or a
  separate loop variable.
- This function is private to the `dunders` module — it does not leave that
  scope; only `type_matches` is shared as a standalone utility.
"""