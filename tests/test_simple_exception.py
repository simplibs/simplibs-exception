import pytest
from typing import Any

from simplibs.exception.SimpleException import SimpleException
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)


def test_basic_construction_and_str_representation():
    """
    Verifies that a basic exception instance can be successfully constructed
    and its string representation correctly reflects the custom metadata label.
    """
    # 1. Initialize the target exception blueprint
    err = SimpleException("boom", label="my-label")

    # 2. Assert text visualization contains core metadata markers
    assert "my-label" in str(err)


def test_can_be_raised_and_caught():
    """
    Validates that the exception correctly hooks into the native Python runtime
    and can be trapped using standard try-except blocks.
    """
    # 1. Trigger the standard raise lifecycle flow
    with pytest.raises(SimpleException):
        raise SimpleException("boom", label="x")


def test_repr_contains_error_name():
    """
    Ensures that the engineering string representation (__repr__) explicitly
    captures and prints the configured custom error type identity.
    """
    # 1. Instantiate exception using a custom system identity name
    err = SimpleException("boom", label="x", error_name="CUSTOM ERROR")

    # 2. Validate engineering layout output format
    assert repr(err) == "<SimpleException(error_name='CUSTOM ERROR')>"


def test_dynamic_exception_type_is_injected_into_mro():
    """
    Validates the core dynamic MRO architecture: when a foreign exception class
    is requested, the instance successfully assumes both identities at runtime.
    """
    # 1. Execute runtime class factory allocation inside the instantiation cycle
    err = SimpleException("boom", label="x", exception=ValueError)

    # 2. Assert multi-inheritance graph integration
    assert isinstance(err, ValueError)
    assert isinstance(err, SimpleException)


def test_with_location_offset_returns_new_instance_with_advanced_depth():
    """
    Verifies that shifting the frame lookup offset generates a new distinct
    exception instance with incremented depth parameters.
    """
    # 1. Construct baseline exception tracking state
    err = SimpleException("boom", label="x", get_location=1)

    # 2. Apply transformation multiplier offset
    new_err = err.with_location_offset(2)

    # 3. Assert deep state replication and mutation isolation
    assert new_err.get_location == 3
    assert new_err is not err


def test_init_subclass_rejects_unknown_attributes_on_subclass():
    """
    Validates architectural validation guards: creating a concrete subclass
    with arbitrary, non-contract variables must immediately raise an internal ecosystem error.
    """
    # 1. Attempt definition of an invalid specification layout
    with pytest.raises(SimpleExceptionInternalError):
        # noinspection PyUnusedLocal
        class BadSubclass(SimpleException):
            totally_made_up_attr = "oops"


def test_init_subclass_allows_valid_overrides():
    """
    Ensures that declarative overrides of contract-defined variables (like error_name)
    are permitted and propagate correctly onto the compiled subclass blueprint.
    """

    # 1. Declare a valid system blueprint subclass specification
    class GoodSubclass(SimpleException):
        error_name: str = "GOOD SUBCLASS ERROR"

    # 2. Validate structural layout inheritance
    assert GoodSubclass.error_name == "GOOD SUBCLASS ERROR"