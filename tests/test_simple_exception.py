import pytest
from simplibs.exception.SimpleException import SimpleException
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)


def test_basic_construction_and_str_representation():
    """Validates construction and that the output renders the provided metadata."""
    err = SimpleException("boom", label="my-label")
    assert "my-label" in str(err)


def test_can_be_raised_and_caught():
    """Confirms native Python exception lifecycle integration."""
    with pytest.raises(SimpleException):
        raise SimpleException("boom", label="x")


def test_repr_contains_error_name():
    """Checks engineering signature for unique class/error identity identification."""
    err = SimpleException("boom", label="x", error_name="CUSTOM")
    assert repr(err) == "<SimpleException(error_name='CUSTOM')>"


def test_dynamic_exception_type_is_injected_into_mro():
    """Verifies that the exception factory successfully injects foreign exceptions into MRO."""
    err = SimpleException("boom", label="x", exception=ValueError)
    assert isinstance(err, ValueError)
    assert isinstance(err, SimpleException)


def test_with_location_offset_returns_new_instance():
    """Validates that cloning/transformation creates a fresh instance without mutating the original."""
    err = SimpleException("boom", label="x", get_location=1)
    new_err = err.with_location_offset(2)

    assert new_err.get_location == 3
    assert new_err is not err


def test_init_subclass_guards():
    """Tests the architectural guardrails against illegal subclass attributes."""
    with pytest.raises(SimpleExceptionInternalError):
        class BadSubclass(SimpleException):
            not_allowed_attr = "oops"


def test_init_subclass_valid_overrides():
    """Confirms that valid system contract overrides are accepted."""

    class GoodSubclass(SimpleException):
        error_name: str = "GOOD_ERROR"

    assert GoodSubclass.error_name == "GOOD_ERROR"