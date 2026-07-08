import pytest
from simplibs.exception.tools.raise_location_offset import raise_location_offset


class _MockAwareError(Exception):
    def __init__(self, tag):
        super().__init__(tag)
        self.offset_applied = None

    def with_location_offset(self, offset=1):
        new = _MockAwareError("cloned")
        new.offset_applied = offset
        return new


def test_transparency_on_success():
    """Verifies the decorator does not interfere with normal function execution."""

    @raise_location_offset()
    def get_val(): return 42

    assert get_val() == 42


def test_offset_mutation_on_error():
    """Ensures the decorator successfully applies the offset to aware exceptions."""

    @raise_location_offset(offset=2)
    def fail():
        raise _MockAwareError("trigger")

    with pytest.raises(_MockAwareError) as exc:
        fail()

    assert exc.value.offset_applied == 2


def test_plain_exception_preservation():
    """Confirms plain exceptions pass through without being wrapped in context."""

    @raise_location_offset()
    def fail():
        raise ValueError("raw")

    with pytest.raises(ValueError) as exc:
        fail()

    assert str(exc.value) == "raw"
    assert exc.value.__suppress_context__ is True


def test_metadata_preservation():
    """Checks that function signatures/docs survive the decoration process."""

    @raise_location_offset()
    def my_func():
        """Docs."""
        pass

    assert my_func.__name__ == "my_func"
    assert my_func.__doc__ == "Docs."