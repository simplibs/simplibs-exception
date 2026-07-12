"""
Tests for assert_function_callable — validation of target execution interfaces.
"""
import pytest
from simplibs.exception.testing.asserts.functions.assert_function_callable import assert_function_callable


# -----------------------------------------------------------------------------
# Test Target Dummies & Mocks
# -----------------------------------------------------------------------------

def regular_function():
    """A standard named python routine."""
    pass


class CallableClassMock:
    """An object matching the callable interface via dunder call decoration."""
    def __call__(self, *args, **kwargs):
        pass


class SubtestNoOpSpy:
    """Zero-overhead dummy tracking stub satisfying subtests contract parameters."""
    def test(self, name: str):
        return self
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_callable_passes_for_valid_execution_interfaces():
    """Verify that named functions, lambdas, and invocable class instances pass cleanly."""
    spy = SubtestNoOpSpy()

    # 1. Standard function reference
    assert assert_function_callable(spy, regular_function, verbose=False) is regular_function

    # 2. Inline lambda routine
    lambda_func = lambda: True
    assert assert_function_callable(spy, lambda_func, verbose=False) is lambda_func

    # 3. Object instance implementing __call__
    callable_instance = CallableClassMock()
    assert assert_function_callable(spy, callable_instance, verbose=False) is callable_instance


def test_callable_fails_for_non_executable_primitives():
    """Verify that passing static primitive variables trips the execution gate early."""
    spy = SubtestNoOpSpy()

    # 1. Raw string primitive payload
    with pytest.raises(AssertionError):
        assert_function_callable(spy, "not-a-function", verbose=False)

    # 2. None token payload
    with pytest.raises(AssertionError):
        assert_function_callable(spy, None, verbose=False)