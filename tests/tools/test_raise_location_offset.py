import pytest

from simplibs.exception.tools.raise_location_offset import raise_location_offset


class _FakeLocationAwareError(Exception):
    """A minimal double that mimics the duck-typed with_location_offset protocol,
    kept independent from the real SimpleException class (which currently
    has a separate, already-documented construction bug)."""

    def __init__(self, tag):
        super().__init__(tag)
        self.tag = tag
        self.offset_applied = None

    def with_location_offset(self, offset=1):
        new = _FakeLocationAwareError(self.tag)
        new.offset_applied = offset
        return new


def test_function_returns_normally_when_no_exception_raised():
    @raise_location_offset()
    def ok():
        return "fine"

    assert ok() == "fine"


def test_default_offset_is_applied_to_location_aware_exception():
    @raise_location_offset()
    def boom():
        raise _FakeLocationAwareError("original")

    with pytest.raises(_FakeLocationAwareError) as exc_info:
        boom()

    assert exc_info.value.offset_applied == 1


def test_custom_offset_is_applied_to_location_aware_exception():
    @raise_location_offset(offset=3)
    def boom():
        raise _FakeLocationAwareError("original")

    with pytest.raises(_FakeLocationAwareError) as exc_info:
        boom()

    assert exc_info.value.offset_applied == 3


def test_plain_exception_without_location_support_is_reraised_unmodified():
    @raise_location_offset()
    def boom():
        raise ValueError("plain error")

    with pytest.raises(ValueError, match="plain error"):
        boom()


def test_reraised_plain_exception_suppresses_original_context():
    @raise_location_offset()
    def boom():
        raise ValueError("plain error")

    with pytest.raises(ValueError) as exc_info:
        boom()

    assert exc_info.value.__suppress_context__ is True


def test_decorator_preserves_function_metadata():
    @raise_location_offset()
    def documented_function():
        """A docstring."""

    assert documented_function.__name__ == "documented_function"
    assert documented_function.__doc__ == "A docstring."
