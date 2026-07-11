import pytest
from simplibs.exception.testing.exceptions_bulk_test import exceptions_bulk_test
from simplibs.exception.testing.containers import TestCase
from simplibs.exception import SimpleExceptionData


# -----------------------------------------------------------------------------
# Test Target Dummies
# -----------------------------------------------------------------------------

class SimpleException(SimpleExceptionData, Exception):
    """Dummy exception satisfying the framework inheritance contract."""

    def __init__(self, message: str = "Error"):
        super().__init__(message=message)


def trigger_error(val):
    if val == "bad":
        raise SimpleException("Error")
    return True


class SubtestNoOpSpy:
    """Mock subtests manager that acts as a container."""

    def test(self, name: str): return self

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb): return False


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_bulk_test_orchestrator_routing():
    """Verify that bulk_test correctly identifies and routes different item shapes."""
    spy = SubtestNoOpSpy()

    matrix = [
        # 1. Raw Exception Class (Routing 2)
        SimpleException,

        # 2. Functional invocation (Routing 3)
        (SimpleException, trigger_error, "bad"),

        # 3. Encapsulated TestCase (Routing 1)
        TestCase(
            func=trigger_error,
            invalid_param=("bad",),
            exception_type=SimpleException
        )
    ]

    # Nyní, když SimpleException dědí ze SimpleExceptionData, routing projde
    exceptions_bulk_test(spy, matrix, verbose=False)


def test_bulk_test_fails_on_unknown_format():
    """Verify that the fallback gate catches unsupported signatures."""
    spy = SubtestNoOpSpy()

    with pytest.raises(AssertionError, match="Unsupported item signature footprint"):
        exceptions_bulk_test(spy, ["nepodporovany_typ"], verbose=False)