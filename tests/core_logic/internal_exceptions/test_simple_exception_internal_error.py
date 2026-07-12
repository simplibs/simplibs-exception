import pytest
from simplibs.exception.testing.assert_exception_class import assert_exception_class
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)


def test_internal_error_basic_contract(subtests):
    """Runs the universal validation suite for inheritance, defaults, constructor and interface."""
    assert_exception_class(
        subtests,
        SimpleExceptionInternalError,
    )


def test_str_contains_rendered_pretty_message():
    """Ensure PRETTY rendering is applied and contains all critical metadata."""
    err = SimpleExceptionInternalError(label="my-label", problem="something broke")
    text = str(err)
    assert "INTERNAL ERROR" in text
    assert "my-label" in text
    assert "something broke" in text


def test_skips_validation_and_never_crashes_on_bad_types():
    """Verify internal errors bypass validation and survive invalid field types."""
    err = SimpleExceptionInternalError(label=12345)  # type: ignore
    assert "12345" in str(err)
