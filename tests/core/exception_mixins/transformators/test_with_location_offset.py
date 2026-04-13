"""
Tests for WithLocationOffsetMixin — data preservation, stack shifting, and edge cases.
"""
import pytest
from simplibs.exception.SimpleException import SimpleException
from simplibs.sentinels import UNSET


# -----------------------------------------------------------------------------
# WithLocationOffset
# -----------------------------------------------------------------------------

class CustomError(SimpleException):
    """Subclass for testing inheritance preservation."""
    error_name = "CUSTOM_ERROR"
    expected = "something"


def test_with_location_offset_preserves_data():
    """The new instance must have identical data and maintain the correct class type."""
    orig = CustomError(
        value=42,
        value_label="answer",
        problem="wrong universe",
        how_to_fix="try 43"
    )

    new_exc = orig.with_location_offset(1)

    assert new_exc.value == 42
    assert new_exc.value_label == "answer"
    assert new_exc.problem == "wrong universe"
    assert new_exc.how_to_fix == ("try 43",)
    assert new_exc.error_name == "CUSTOM_ERROR"
    assert isinstance(new_exc, CustomError)


def test_with_location_offset_keeps_unset_as_unset():
    """UNSET values must remain UNSET in the new instance, not converted to None."""
    orig = SimpleException(problem="just a problem")
    new_exc = orig.with_location_offset(1)

    assert new_exc.value is UNSET
    assert new_exc.expected is UNSET
    assert new_exc.problem == "just a problem"


def test_stack_location_shift():
    """The exception message must point to the caller's line when offset is applied."""

    def internal_library_helper():
        # Simulate library internals
        e = SimpleException(problem="error inside")
        # Shift offset to target the caller of this helper
        return e.with_location_offset(1)

    # Calling the helper - this specific line should appear in 'File info'
    exc = internal_library_helper()
    message = str(exc)

    # Verification that the internal helper is skipped in the output
    assert "internal_library_helper" not in message
    assert "test_stack_location_shift" in message


def test_with_location_offset_disabled_location():
    """If get_location is False, applying an offset should not enable it."""
    orig = SimpleException(problem="no loc", get_location=False)
    new_exc = orig.with_location_offset(5)

    assert new_exc._get_location is False


def test_multiple_offsets_stacking():
    """Multiple calls to with_location_offset should increment the total depth."""
    # Default get_location is True (evaluated as 1 in math contexts)
    orig = SimpleException(get_location=True)
    new_exc = orig.with_location_offset(1).with_location_offset(1)

    # 1 (base) + 1 + 1 = 3
    assert new_exc._get_location == 3