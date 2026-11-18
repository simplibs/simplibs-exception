"""
Tests for exceptions_bulk_test — the tuple form `(ExceptionClass, function, *params)`.
"""
from functools import partial

from simplibs.exception import SimpleExceptionData
from simplibs.exception.testing import Kwargs
from simplibs.exception.testing.bulk_test.exceptions_bulk_test import exceptions_bulk_test


class SimpleException(SimpleExceptionData, Exception):
    """Dummy exception satisfying the framework inheritance contract."""

    def __init__(self, message: str = "Error"):
        super().__init__(message=message)


class SubtestNoOpSpy:
    """Mock subtests manager that acts as a container."""

    def test(self, name: str): return self
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False


def raises_without_arguments():
    raise SimpleException("Error")


def raises_for_bad(val):
    if val == "bad":
        raise SimpleException("Error")
    return True


def raises_for_bad_keyword(*, val):
    if val == "bad":
        raise SimpleException("Error")
    return True


def test_tuple_without_params_calls_the_function_without_arguments():
    """Verify that (ExcClass, func) is a valid item for a function that takes no arguments."""
    exceptions_bulk_test(SubtestNoOpSpy(), [(SimpleException, raises_without_arguments)], verbose=False)


def test_tuple_accepts_a_callable_without_a_name():
    """Verify that a partial (no __name__) is accepted and named by its type."""
    item = (SimpleException, partial(raises_for_bad, "bad"))

    exceptions_bulk_test(SubtestNoOpSpy(), [item], verbose=False)


def test_tuple_with_trailing_kwargs_passes_keyword_arguments():
    """Verify that a trailing Kwargs is expanded into keyword arguments."""
    item = (SimpleException, raises_for_bad_keyword, Kwargs(val="bad"))

    exceptions_bulk_test(SubtestNoOpSpy(), [item], verbose=False)
