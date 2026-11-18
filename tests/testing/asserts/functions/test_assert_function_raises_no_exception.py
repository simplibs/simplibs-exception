"""
Tests for assert_function_raises — the Framework Guard for a function that raises nothing in verbose mode.
"""
from contextlib import contextmanager

import pytest
from _pytest.outcomes import Failed

from simplibs.exception.testing.asserts.functions.assert_function_raises import assert_function_raises


class SwallowingSubtests:
    """Stands in for the real subtests fixture: a failing check is recorded and the test goes on."""

    def __init__(self) -> None:
        self.failed: list[str] = []

    @contextmanager
    def test(self, name: str):
        try:
            yield
        except (Exception, Failed):
            self.failed.append(name)


def returns_normally(value):
    return "success"


def test_verbose_mode_reports_a_function_that_raises_nothing_with_a_clear_message():
    """Verify that verbose=True ends in the Framework Guard, not in an error from an empty pytest.raises."""
    subtests = SwallowingSubtests()

    with pytest.raises(Failed, match="did not raise any exception"):
        assert_function_raises(subtests, returns_normally, invalid_params=("anything",), verbose=True)

    # the failed check was still recorded by its own subtest before the guard stopped the test
    assert subtests.failed == ["test_raises_exception"]


def test_verbose_mode_guard_names_the_called_arguments():
    """Verify that the guard message says how the function was called."""
    with pytest.raises(Failed, match="args=\\('anything',\\)"):
        assert_function_raises(SwallowingSubtests(), returns_normally, invalid_params=("anything",), verbose=True)
