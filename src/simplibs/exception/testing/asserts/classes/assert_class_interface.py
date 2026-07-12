from typing import Any
# Outers
from ...tools import maybe_subtest


def assert_class_interface(
    subtests: Any,
    exc_class: type[Any],
    *,
    verbose: bool = True,
    intro: str = "",
) -> Any:
    """Assert that an exception class exposes the expected public interface.

    Instantiates the exception class and verifies the availability and basic
    functionality of the standard public API.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        exc_class: Exception class to validate.
        verbose: Enables pytest subtests.
        intro: Optional prefix added to generated subtest names.

    Returns:
        The instantiated exception object.
    """
    subintro = "test_class_interface::"

    # Instantiate via raw parameterless initialization to test interface defaults
    exc = exc_class()

    # 1. Verify standard string representation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_str",
        verbose=verbose,
    ):
        assert isinstance(str(exc), str)

    # 2. Verify developer-focused string representation
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_repr",
        verbose=verbose,
    ):
        assert isinstance(repr(exc), str)

    # 3. Verify core telemetry dictionary export
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_to_dict",
        verbose=verbose,
    ):
        assert isinstance(exc.to_dict(), dict)

    # 4. Verify enriched debug dictionary export
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_to_debug_dict",
        verbose=verbose,
    ):
        assert isinstance(exc.to_debug_dict(), dict)

    # 5. Verify string-serialized JSON export payload
    with maybe_subtest(
        subtests,
        name=f"{intro}{subintro}test_to_json",
        verbose=verbose,
    ):
        assert isinstance(exc.to_json(), str)

    return exc


_DESIGN_NOTES = """
# assert_class_interface (Public API Interface Check)

## Purpose
Acts as the contract enforcement gate for the exception's public-facing interface. It ensures that any 
custom exception class correctly implements, preserves, and executes the entire suite of required 
dunder formatting types and serializátor data-export channels.

## Operational Verification Matrix
The suite validates that the runtime execution outputs adhere strictly to the expected type specifications:
- **`str(exc)` & `repr(exc)`:** Must yield valid string primitives, guaranteeing seamless integration 
  with terminal loggers, print routines, and trace representation engines.
- **`to_dict()`:** Must yield a standard dictionary containing the baseline telemetry properties.
- **`to_debug_dict()`:** Must yield an extended telemetry dictionary containing frame stack parameters 
  and deeper metadata tracking variables.
- **`to_json()`:** Must return a valid serialized string block ready for across-the-wire JSON transmissions 
  or automated file storage dumps.

## Pipeline Integration Value
This routine focuses purely on **type compliance** rather than deep message content auditing. By separating 
the superficial API contract validation from granular attribute string checks, it allows the master 
orchestrators to pinpoint architectural method omission errors instantly before downstream content logic 
scans are executed.
"""