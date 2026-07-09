from typing import Any
from simplibs.sentinels import UNSET
# Outers
from ....SimpleExceptionData import SimpleExceptionData
from ...assert_exception_class import assert_exception_class
from ..common.maybe_subtest import maybe_subtest


def deep_test_exception_class(
    subtests: Any,
    exc_class: type[Any],
    *,
    verbose: bool,
) -> None:
    """Execute a comprehensive structural and architectural audit on an exception class.

    Verifies inheritance compliance, safe zero-argument constructor instantiation,
    default class-level state values, string rendering stability, and dictionary
    serialization capabilities.
    """

    end_checkpoint_name = f"{exc_class.__name__}::deep_test_end"

    with maybe_subtest(subtests, name=end_checkpoint_name, verbose=verbose):
        # 1. Enforce framework sub-typing compliance matrix
        assert issubclass(exc_class, SimpleExceptionData), (
            f"{exc_class.__name__} violates architectural contract: "
            f"must be a subclass of SimpleExceptionData."
        )

        class_dict = exc_class.__dict__
        namespace_intro = f"{exc_class.__name__}::"

        # 2. Audit class-level static field defaults via reflection mapping
        # noinspection PyTypeChecker
        assert_exception_class(
            subtests,
            exc_class,
            error_name=class_dict.get("error_name", UNSET),
            label=class_dict.get("label", UNSET),
            expected=class_dict.get("expected", UNSET),
            value=class_dict.get("value", UNSET),
            problem=class_dict.get("problem", UNSET),
            context=class_dict.get("context", UNSET),
            how_to_fix=class_dict.get("how_to_fix", UNSET),
            exception=class_dict.get("exception", UNSET),
            get_location=class_dict.get("get_location", UNSET),
            skip_locations=class_dict.get("skip_locations", UNSET),
            oneline=class_dict.get("oneline", UNSET),
            verbose=verbose,
            intro=namespace_intro,
        )

        # 3. Instantiate exception instance via standard zero-argument interface
        exc = exc_class()

        # 4. Verify formatting/rendering pipeline consistency
        with maybe_subtest(subtests, name=f"{exc_class.__name__}::test_renderer", verbose=verbose):
            assert isinstance(str(exc), str)

        # 5. Verify telemetry data export capabilities (to_dict)
        if hasattr(exc, "to_dict"):
            with maybe_subtest(subtests, name=f"{exc_class.__name__}::test_to_dict", verbose=verbose):
                assert isinstance(exc.to_dict(), dict)

        # 6. Verify deep troubleshooting export capabilities (to_debug_dict)
        if hasattr(exc, "to_debug_dict"):
            with maybe_subtest(subtests, name=f"{exc_class.__name__}::test_to_debug_dict", verbose=verbose):
                assert isinstance(exc.to_debug_dict(), dict)


_DESIGN_NOTES = """
# deep_test_exception_class (Architectural Auditor)

## Purpose
An advanced internal testing proxy designed to conduct rigorous compliance audits on exception 
classes. It moves beyond standard shallow value checks to guarantee that target objects safely fulfill 
the deep structural and behavior contracts mandated by the `SimpleExceptionData` ecosystem.

## Execution Matrix & Verification Layers

### 1. Blueprint Integrity
The runner applies strict subclass verification against `SimpleExceptionData`. It extracts internal 
metadata using Python's static class dictionary mapping (`__dict__.get(...)`) to securely pass 
unmodified default definitions to the secondary validation loops without triggering unwanted mutations.

### 2. Functional Pipeline Soundness
The utility tests zero-argument construction to guarantee safe object initialization lifecycle passes. 
It confirms that string serialization triggers an evaluation sequence that outputs strings, and safely 
inspects optional standard data serialization channels (`to_dict` and `to_debug_dict`) when exported 
by the target instance.
"""