import pytest

from simplibs.exception.tools.raise_with_location_offset import (
    raise_with_location_offset,
)


class _FakeLocationAwareError(Exception):
    def __init__(self, tag):
        super().__init__(tag)
        self.tag = tag
        self.offset_applied = None

    def with_location_offset(self, offset=1):
        new = _FakeLocationAwareError(self.tag)
        new.offset_applied = offset
        return new


def test_raises_the_result_of_with_location_offset_for_supporting_exceptions():
    exc = _FakeLocationAwareError("original")

    with pytest.raises(_FakeLocationAwareError) as exc_info:
        raise_with_location_offset(exc, offset=1)

    assert exc_info.value.offset_applied == 1


def test_default_offset_is_one():
    exc = _FakeLocationAwareError("original")

    with pytest.raises(_FakeLocationAwareError) as exc_info:
        raise_with_location_offset(exc)

    assert exc_info.value.offset_applied == 1


def test_custom_offset_is_forwarded():
    exc = _FakeLocationAwareError("original")

    with pytest.raises(_FakeLocationAwareError) as exc_info:
        raise_with_location_offset(exc, offset=7)

    assert exc_info.value.offset_applied == 7


def test_plain_exception_without_location_support_is_raised_as_is():
    exc = ValueError("plain error")

    with pytest.raises(ValueError) as exc_info:
        raise_with_location_offset(exc)

    assert exc_info.value is exc


def test_always_raises_never_returns():
    exc = ValueError("plain error")
    with pytest.raises(ValueError):
        raise_with_location_offset(exc)
