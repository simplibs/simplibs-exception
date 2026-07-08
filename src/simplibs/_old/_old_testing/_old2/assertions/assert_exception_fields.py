from typing import Any
from simplibs.sentinels import MISSING


def assert_exception_fields(
    exc: BaseException,
    expected: dict[str, Any],
) -> None:
    """
    Verifies that selected attributes on a caught exception instance match
    the expected values. Only the keys present in `expected` are checked —
    everything else on the exception is ignored.

    This is the lowest-level building block of the testing helpers: every
    other assertion in this package that needs to compare exception
    attributes delegates to this function, so the failure-message format
    stays consistent everywhere.

    Args:
        exc: The caught exception instance (typically a SimpleException
             or one of its subclasses, but any object works — attributes
             are read via plain `getattr`).
        expected: Mapping of {attribute_name: expected_value}.

    Raises:
        AssertionError: If any actual attribute value differs from the
                        expected one. The message includes the exception's
                        full debug snapshot (via `to_debug_dict()`, if
                        available) so the mismatch can be diagnosed without
                        re-running the test with extra prints.
    """

    # 1. Cyklus skrze položkyvýjimky
    for field_name, expected_value in expected.items():

        # 2. Načtení hodnoty
        actual_value = getattr(exc, field_name, MISSING)

        # 3. Pokud hodnota nebyla nalezena
        if actual_value is MISSING:
            raise AssertionError(
                f"Exception of type '{type(exc).__name__}' has no attribute "
                f"'{field_name}' to check."
            )

        # 4. Pokud se hodnota neschoduje s očekávanou
        if actual_value != expected_value:
            debug_info = (
                exc.to_debug_dict()
                if hasattr(exc, "to_debug_dict")
                else repr(exc)
            )
            raise AssertionError(
                f"Exception field '{field_name}' mismatch.\n"
                f"Expected: {expected_value!r}\n"
                f"Got:      {actual_value!r}\n"
                f"Full exception state: {debug_info}"
            )

