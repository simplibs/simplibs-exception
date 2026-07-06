import pytest
from simplibs.exception.SimpleException import SimpleException
from simplibs.exception.tools.bool_or_exception import bool_or_exception


def test_return_bool_true_short_circuits_to_false():
    """
    Ensures that when return_bool is active (True), the evaluation engine
    instantly short-circuits and returns False, avoiding exception generation.
    """
    result = bool_or_exception(True, message="never raised", label="x")
    assert result is False


def test_return_bool_true_ignores_all_other_kwargs():
    """
    Verifies that the short-circuit pathway remains completely unaffected
    even if extra keyword configuration arguments are supplied.
    """
    result = bool_or_exception(
        True,
        message="whatever",
        value=123,
        label="x",
        expected="y",
        problem="z",
    )
    assert result is False


def test_return_bool_false_raises_configured_simple_exception():
    """
    Validates the standard routine error pathway: when return_bool is False,
    the tool properly generates and throws a fully populated SimpleException.
    """
    # 1. Assert that the helper correctly converts input data parameters into a raised instance
    with pytest.raises(SimpleException) as exc_info:
        bool_or_exception(False, message="boom", label="x")

    # 2. Verify state retention on the caught exception context object
    assert exc_info.value.message == "boom"
    assert exc_info.value.label == "x"