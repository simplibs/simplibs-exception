import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.validate_location_blacklist import (
    validate_location_blacklist,
)


def test_empty_tuple_is_valid():
    """Confirms that an empty tuple is fully accepted, indicating no custom user-level file exclusions."""
    assert validate_location_blacklist(()) is None


def test_tuple_of_strings_is_valid():
    """Validates that a tuple consisting entirely of raw strings passes inspection successfully."""
    assert validate_location_blacklist(("a.py", "b.py")) is None


def test_non_tuple_raises():
    """
    Guarantees that other iterable collections (like lists) are blocked fast,
    enforcing an immutable data boundary for the trace engine.
    """
    with pytest.raises(SimpleExceptionSettingsError):
        validate_location_blacklist(["a.py", "b.py"])


def test_tuple_with_non_string_items_raises():
    """
    Verifies the Element Deep-Scan pattern: any invalid data types inside the tuple
    must be aggregated and reported simultaneously within the error payload.
    """
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        validate_location_blacklist(("a.py", 123, None))

    # The exception must collect and expose all offending elements at once
    assert exc_info.value.value == [123, None]


def test_string_instead_of_tuple_raises():
    """Ensures that passing a raw string instead of an enclosed tuple is intercepted before it can pollute the engine."""
    with pytest.raises(SimpleExceptionSettingsError):
        validate_location_blacklist("a.py")


def test_error_payload_contains_accurate_deep_scan_counts():
    """
    Architectural Contract: Verifies that the raised exception dynamically tracks
    and states the exact number of type-polluting items found during the deep-scan cycle.
    """
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        # Supplying exactly 3 invalid non-string items
        validate_location_blacklist((1, 2, 3))

    err = exc_info.value

    assert err.label == "LOCATION_BLACKLIST"
    # Ensure the dynamic counter injected the correct number into the diagnostics
    assert "found 3 invalid item(s)" in err.problem