import pytest
from simplibs.exception.tools.raise_with_location_offset import raise_with_location_offset


class _MockAwareError(Exception):
    """Mok pro ověření, že utility správně volá with_location_offset."""

    def __init__(self, tag):
        super().__init__(tag)
        self.offset_applied = None

    def with_location_offset(self, offset=1):
        new = _MockAwareError("cloned")
        new.offset_applied = offset
        return new


def test_mutation_for_aware_exceptions():
    """Confirms that exceptions supporting the offset API are properly cloned/mutated."""
    exc = _MockAwareError("original")
    with pytest.raises(_MockAwareError) as exc_info:
        raise_with_location_offset(exc, offset=5)

    assert exc_info.value.offset_applied == 5


def test_standard_exception_passthrough():
    """Validates that plain exceptions are raised directly without side effects."""
    exc = TypeError("oops")
    with pytest.raises(TypeError) as exc_info:
        raise_with_location_offset(exc)

    assert exc_info.value is exc


def test_always_terminates_execution():
    """Confirms that the utility always raises an exception and never returns a value."""
    with pytest.raises(RuntimeError):
        raise_with_location_offset(RuntimeError("terminate"))