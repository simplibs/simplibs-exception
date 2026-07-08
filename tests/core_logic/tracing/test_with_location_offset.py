from simplibs.exception._core_logic.tracing.with_location_offset import (
    with_location_offset,
)
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)


# NOTE: We deliberately use SimpleExceptionInternalError (not SimpleException)
# as the subject here. with_location_offset() builds a new instance via
# `type(instance)(...)`, and SimpleException.__new__ currently has a known
# separate lifecycle constraint that makes constructing SimpleException directly raise.
# SimpleExceptionInternalError does not override __new__, allowing isolated testing.


def test_bool_true_get_location_advances_by_offset():
    """Confirms that a boolean True location trigger evaluates as baseline depth 1 and successfully increments by the offset."""
    original = SimpleExceptionInternalError(label="x", get_location=True)
    new = with_location_offset(original, offset=2)
    assert new.get_location == 3


def test_bool_false_get_location_stays_false():
    """Validates that if location tracing was explicitly disabled (False), it remains firmly False regardless of the offset."""
    original = SimpleExceptionInternalError(label="x", get_location=False)
    new = with_location_offset(original, offset=5)
    assert new.get_location is False


def test_int_get_location_advances_by_offset():
    """Ensures that an already specific integer depth is correctly shifted deeper into the runtime stack by standard arithmetic addition."""
    original = SimpleExceptionInternalError(label="x", get_location=4)
    new = with_location_offset(original, offset=2)
    assert new.get_location == 6


def test_default_offset_is_one():
    """Verifies that when no offset argument is provided, the advancement delta defaults strictly to 1 frame."""
    original = SimpleExceptionInternalError(label="x", get_location=1)
    new = with_location_offset(original)
    assert new.get_location == 2


def test_returns_new_instance_of_the_same_class():
    """
    Architectural Contract: Guarantees immutability and subclass preservation. The utility
    must spawn a brand-new distinct instance while perfectly preserving the exact concrete class type.
    """
    original = SimpleExceptionInternalError(label="x")
    new = with_location_offset(original)

    assert type(new) is type(original)
    assert new is not original


def test_preserves_all_other_payload_fields():
    """Validates full data integrity pass-through: all original exception metadata fields must map cleanly into the new instance."""
    original = SimpleExceptionInternalError(
        label="orig-label",
        message="orig-msg",
        problem="orig-problem",
        expected="orig-expected",
        context="orig-context",
        how_to_fix="orig-fix",
        error_name="ORIG ERROR",
    )
    new = with_location_offset(original, offset=1)

    assert new.label == "orig-label"
    assert new.message == "orig-msg"
    assert new.problem == "orig-problem"
    assert new.expected == "orig-expected"
    assert new.context == "orig-context"
    assert new.how_to_fix == "orig-fix"
    assert new.error_name == "ORIG ERROR"


def test_preserves_unset_sentinel_boundaries_during_cloning():
    """
    Architectural Integration Case: Verifies that fields holding the internal UNSET token
    pass through the instantiation factory completely unmodified, preserving filtration boundaries.
    """
    from simplibs.sentinels import UNSET

    # Instantiate an error with a mixture of explicit fields and UNSET fields
    original = SimpleExceptionInternalError(label="defined-label")

    # Value was not provided, so it should be UNSET internally
    assert original.value is UNSET

    # Execute the location offset shift operation
    new = with_location_offset(original, offset=1)

    # Assert that the UNSET token was preserved and did not coerce into None or a fallback string
    assert new.value is UNSET
    assert new.label == "defined-label"