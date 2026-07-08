"""
Tests for check_exception_fields — sentinel-driven selective evaluation and field assertion routing.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.testing._helpers.assertions.check_exception_fields import check_exception_fields


# -----------------------------------------------------------------------------
# Test Doubles & Mocks
# -----------------------------------------------------------------------------

class DummyException:
    """Mock exception instance holding arbitrary state fields."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class SubtestSpy:
    """Mock mirroring pytest-subtests behavior to record executed subtest names."""
    def __init__(self):
        self.called_subtests = []

    def test(self, name):
        """Implements the subtests.test(name) interface required by maybe_subtest."""
        self.called_subtests.append(name)
        return self  # Acts as the context manager itself

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Do not suppress exceptions, allow assertion errors to bubble up to pytest
        return False


# -----------------------------------------------------------------------------
# Evaluation Strategy Tests
# -----------------------------------------------------------------------------

def test_unset_fields_are_skipped():
    """Fields remaining UNSET must be completely ignored by the validator."""
    spy = SubtestSpy()
    exc = DummyException(error_name="CRITICAL", value=123, oneline=True)

    check_exception_fields(spy, exc)

    # No expectations provided -> no subtests executed
    assert spy.called_subtests == []


def test_explicit_fields_are_evaluated_and_pass():
    """Provided expectations must route to correct subtests and pass when matching."""
    spy = SubtestSpy()
    exc = DummyException(
        error_name="VALIDATION ERROR",
        label="age",
        message="Too old",
        expected="positive int",
        value=-5,
        problem="negative value",
        context=("local", "test"),
        how_to_fix="make positive",
        exception=ValueError,
        get_location=True,
        skip_locations=("utils.py",),
        oneline=False
    )

    check_exception_fields(
        subtests=spy,
        exc=exc,
        error_name="VALIDATION ERROR",
        label="age",
        message="Too old",
        expected="positive int",
        value=-5,
        problem="negative value",
        context=("local", "test"),
        how_to_fix="make positive",
        exception=ValueError,
        get_location=True,
        skip_locations=("utils.py",),
        oneline=False,
        intro="prefix_"
    )

    # Check that all subtests were registered with the correct intro prefix
    expected_subtests = [
        "prefix_test_error_name", "prefix_test_label", "prefix_test_message",
        "prefix_test_expected", "prefix_test_value", "prefix_test_problem",
        "prefix_test_context", "prefix_test_how_to_fix", "prefix_test_exception",
        "prefix_test_get_location", "prefix_test_skip_locations", "prefix_test_oneline"
    ]
    assert spy.called_subtests == expected_subtests


def test_field_mismatch_triggers_assertion_error():
    """Any mismatch between expected criteria and exception state must fail."""
    spy = SubtestSpy()
    exc = DummyException(error_name="ERROR", value=100)

    # Mismatch in strict field (value)
    with pytest.raises(AssertionError):
        check_exception_fields(spy, exc, value=200)

    # Mismatch in string field (error_name)
    with pytest.raises(AssertionError):
        check_exception_fields(spy, exc, error_name="DIFFERENT")


def test_exact_match_configuration_propagation():
    """Verify that exact_match parameter affects string evaluations correctly."""
    spy = SubtestSpy()
    exc = DummyException(problem="bad type signature")

    # Fuzzy mode (exact_match=False) should pass on partial substring
    check_exception_fields(spy, exc, problem="signature", exact_match=False)

    # Strict mode (exact_match=True) must fail on partial substring
    with pytest.raises(AssertionError):
        check_exception_fields(spy, exc, problem="signature", exact_match=True)