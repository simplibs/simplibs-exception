from simplibs.exception._core_logic.lifecycle.init_utils.process_get_location import (
    process_get_location,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


def test_bool_true_is_passed_through():
    """Ensures that a raw True boolean flag is passed through completely un-mutated."""
    assert process_get_location(True) is True


def test_bool_false_is_passed_through():
    """Ensures that a raw False boolean flag is passed through completely un-mutated."""
    assert process_get_location(False) is False


def test_int_is_passed_through():
    """Validates that a explicit custom stack depth integer is retained as-is."""
    assert process_get_location(3) == 3


def test_invalid_value_falls_back_to_settings_default():
    """Guarantees that supplying an invalid data type triggers a silent fallback to the global settings state."""
    assert process_get_location("not-valid") == SimpleExceptionSettings.GET_LOCATION


def test_none_falls_back_to_settings_default():
    """Confirms that explicit None states are treated as unconfigured triggers, reverting to global settings."""
    assert process_get_location(None) == SimpleExceptionSettings.GET_LOCATION


def test_reflects_changed_settings_default():
    """
    Verifies dynamic runtime tracking: modifying the central SimpleExceptionSettings.GET_LOCATION
    value on the fly must immediately reflect inside downstream resolution flows.
    """
    # 1. Simulate hot-swapping the central framework settings manager state
    SimpleExceptionSettings.GET_LOCATION = 5

    # 2. Assert that the resolver mirrors the dynamic update instantly
    assert process_get_location(None) == 5


def test_boundary_integer_values_pass_through_successfully():
    """
    Architectural Edge Case: Verifies that boundary integer constraints (like zero and
    negative stack offsets) are fully permitted by the type inspector and pass through cleanly.
    """
    # Zero is a critical valid frame marker (current context caller execution block)
    assert process_get_location(0) == 0

    # Negative integers must pass un-mutated as well if used for relative stack shifts
    assert process_get_location(-2) == -2