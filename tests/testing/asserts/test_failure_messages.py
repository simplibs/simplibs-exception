"""
Tests for the failure messages of the low-level assertions.

The package is installed, so pytest does not rewrite its plain `assert` statements: without
an explicit message a failure would be empty. These tests pin that every failure says what was expected.
"""
import pytest

from simplibs.exception.testing.asserts.classes.assert_class_inheritance import assert_class_inheritance
from simplibs.exception.testing.asserts.fields._utils.compare_strings import compare_strings
from simplibs.exception.testing.asserts.fields._utils.compare_values import compare_values
from simplibs.exception.testing.asserts.functions.assert_function_callable import assert_function_callable


class SubtestNoOpSpy:
    """Mock subtests manager that acts as a container."""

    def test(self, name: str): return self
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False


def test_compare_strings_exact_failure_names_the_field():
    with pytest.raises(AssertionError, match=r"Expected message to equal .*got"):
        compare_strings("abc", "xyz", exact_match=True, field="message")


def test_compare_strings_startswith_failure_names_the_field():
    with pytest.raises(AssertionError, match=r"Expected label to start with .*got"):
        compare_strings("abc", "xyz", startswith=True, field="label")


def test_compare_strings_contains_failure_names_the_field():
    with pytest.raises(AssertionError, match=r"Expected problem to contain .*got"):
        compare_strings("abc", "xyz", field="problem")


def test_compare_strings_field_defaults_to_value():
    with pytest.raises(AssertionError, match=r"Expected value to equal"):
        compare_strings("abc", "xyz", exact_match=True)


def test_compare_values_failure_names_the_field():
    with pytest.raises(AssertionError, match=r"Expected code to equal 1, got 2"):
        compare_values(1, 2, field="code")


def test_function_callable_failure_names_the_type():
    with pytest.raises(AssertionError, match=r"Expected a callable, got str"):
        assert_function_callable(SubtestNoOpSpy(), "not-callable", verbose=False)


def test_class_inheritance_given_a_non_class_fails_with_a_message_not_a_type_error():
    """Verify that passing something that is not a class is a failed check, not a TypeError from issubclass."""
    with pytest.raises(AssertionError, match="BaseException"):
        assert_class_inheritance(SubtestNoOpSpy(), "not-a-class", verbose=False)
