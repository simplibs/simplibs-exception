from typing import Any
# Inners
from .classes import (
    assert_class_defaults,
    assert_class_constructor,
    assert_class_interface,
    assert_class_inheritance
)


def assert_exception_class(
    subtests: Any,
    exc_class: type[Any],
    *,
    exact_match: bool = True,
    verbose: bool = True,
    verbose_constructor: bool = False,
    intro: str = "",
    deep_check: bool = True,
) -> Any:
    """Execute a complete validation suite for an exception class.

    Runs all available structural, constructor, default-value, and interface
    checks against the supplied exception class using a rigid sequential pipeline.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to validate.
        exact_match: Enables fuzzy comparison lookups when False.
        verbose: Enables pytest subtests separation for standard modules. Acts as a master
            gate that completely overrides and suppresses verbose_constructor when False.
        verbose_constructor: If True, expands individual internal constructor field checks
            into independent pytest subtest keys, provided that global verbose is also True.
            Defaults to False to prevent log clutter.
        intro: Optional prefix added to generated subtest names.
        deep_check: If True, triggers advanced explicit constructor propagation
            and serializer API interface audits.

    Returns:
        The instantiated exception object captured during the defaults verification run.
    """

    # 1. Verify inheritance hierarchy contract (Fail-Fast gate)
    assert_class_inheritance(
        subtests,
        exc_class,
        verbose=verbose,
        intro=intro
    )

    # 2. Verify class-level default values and grab a vanilla instance
    exc = assert_class_defaults(
        subtests,
        exc_class,
        exact_match=exact_match,
        verbose=verbose,
        intro=intro
    )

    # Execute extended structural audits under deep checking conditions
    if deep_check:

        # 3. Verify explicit constructor propagation with dynamic telemetry payloads.
        # Master cascade logic: verbose_constructor is active ONLY IF global verbose is True.
        assert_class_constructor(
            subtests,
            exc_class,
            verbose=verbose and verbose_constructor,
            intro=intro
        )

        # 4. Verify public object API, dunder formatting, and serializers type integrity
        assert_class_interface(
            subtests,
            exc_class,
            verbose=verbose,
            intro=intro
        )

    return exc


_DESIGN_NOTES = """
# assert_exception_class (Composite Exception Class Auditor)

## Purpose
Implements an architectural Facade Pattern that orchestrates a complete, multi-stage compliance matrix 
against any custom framework exception class definition. It serves as the primary master gateway 
used by high-level automated matrix test runners (`bulk_tests.py`).

## Verbosity Hierarchy & Cascading Gate Logic
To balance telemetry depth with test report cleanliness, this engine introduces a two-tier verbosity 
hierarchy that isolates the massive constructor property check lane:

1. **The Master Gate (`verbose`):** Governs the entire pipeline. If `verbose=False`, a strict global 
   silence condition is enforced across all sub-modules. The vnitřní expression `verbose and verbose_constructor` 
   guarantees that the constructor subtests are hard-suppressed, bypassing any local overrides.
2. **The Local Fine-Tuning Gate (`verbose_constructor`):** Specifically addresses the constructor audit 
   which verifies over 10 independent framework properties. 
   - **`False` (Default):** The entire constructor block executes inside a single atomic assertion lane. 
     This keeps bulk matrix execution logs free from extensive visual clutter.
   - **`True`:** Expands each internal property check into an independent subtest key. This is a premium 
     debugging mechanism designed to be manually toggled when a constructor propagation test fails 
     and the developer needs to pinpoint exactly which telemetry string was corrupted or dropped.
"""