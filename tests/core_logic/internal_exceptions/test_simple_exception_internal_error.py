import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionInternalError import (
    SimpleExceptionInternalError,
)


def test_is_exception_subclass():
    """Ensures that the internal error correctly inherits from the native Python Exception class."""
    assert issubclass(SimpleExceptionInternalError, Exception)


def test_default_error_name():
    """Validates that the class has its declarative error identity correctly set to INTERNAL ERROR."""
    err = SimpleExceptionInternalError(label="x")
    assert err.error_name == "INTERNAL ERROR"


def test_can_be_raised_and_caught():
    """Verifies that the internal error integrates natively into Python's try-except lifecycle handling."""
    with pytest.raises(SimpleExceptionInternalError):
        raise SimpleExceptionInternalError(label="boom")


def test_str_contains_rendered_pretty_message():
    """
    Guarantees that string conversion automatically triggers the lazy PRETTY mode
    rendering engine and contains all critical core metadata segments.
    """
    # 1. Instantiate error payload with standard descriptors
    err = SimpleExceptionInternalError(label="my-label", problem="something broke")
    text = str(err)

    # 2. Assert structural visual text block contents
    assert "INTERNAL ERROR" in text
    assert "my-label" in text
    assert "something broke" in text


def test_no_extra_positional_message_argument_required():
    """
    Confirms the pure dataclass constructor API contract: unlike the public exception layer,
    internal errors assign values directly via keyword fields without custom message parsing.
    """
    err = SimpleExceptionInternalError(label="label-only")
    assert err.label == "label-only"


def test_skips_validation_and_never_crashes_on_bad_types():
    """
    Architectural Edge Case: Verifies that internal errors skip protocol validation
    and degrade gracefully. Even if invalid data types are passed during a critical failure,
    the exception must construct successfully without throwing validation errors.
    """
    # Passing an integer into a field typed as str | None to simulate a corrupted state
    # noinspection PyTypeChecker
    err = SimpleExceptionInternalError(label=12345)  # type: ignore

    # The construction must pass and formatting must fall back to standard string conversion
    assert "12345" in str(err)