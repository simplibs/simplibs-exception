from simplibs.exception._core_logic.tracing.with_location_offset import (
    with_location_offset,
)
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)

# NOTE: we deliberately use SimpleExceptionInternalError (not SimpleException)
# as the subject here. with_location_offset() builds a new instance via
# `type(instance)(...)`, and SimpleException.__new__ currently has a known,
# separately-documented bug (see test_add_exception_type.py) that makes
# constructing SimpleException directly raise. SimpleExceptionInternalError
# does not override __new__, so it lets us test this function's own logic
# in isolation.


def test_bool_true_get_location_advances_by_offset():
    original = SimpleExceptionInternalError(label="x", get_location=True)
    new = with_location_offset(original, offset=2)
    assert new.get_location == 3  # True behaves as 1, plus offset


def test_bool_false_get_location_stays_false():
    original = SimpleExceptionInternalError(label="x", get_location=False)
    new = with_location_offset(original, offset=5)
    assert new.get_location is False


def test_int_get_location_advances_by_offset():
    original = SimpleExceptionInternalError(label="x", get_location=4)
    new = with_location_offset(original, offset=2)
    assert new.get_location == 6


def test_default_offset_is_one():
    original = SimpleExceptionInternalError(label="x", get_location=1)
    new = with_location_offset(original)
    assert new.get_location == 2


def test_returns_new_instance_of_the_same_class():
    original = SimpleExceptionInternalError(label="x")
    new = with_location_offset(original)
    assert type(new) is type(original)
    assert new is not original


def test_preserves_all_other_payload_fields():
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
