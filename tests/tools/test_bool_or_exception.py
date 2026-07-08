import pytest
from simplibs.exception.SimpleException import SimpleException
from simplibs.exception.tools.bool_or_exception import bool_or_exception


def test_return_bool_true_short_circuits_to_false():
    """Confirms short-circuit logic: immediately returns False without side effects."""
    result = bool_or_exception(True, message="should not matter")
    assert result is False


def test_return_bool_true_ignores_config():
    """Ensures extra arguments don't trigger exception logic when return_bool is active."""
    result = bool_or_exception(True, message="ignorable", label="ignored")
    assert result is False


def test_return_bool_false_raises_exception():
    """Validates that standard error flow constructs and raises the SimpleException."""
    with pytest.raises(SimpleException) as exc:
        bool_or_exception(False, message="boom", label="x")

    assert exc.value.message == "boom"
    assert exc.value.label == "x"


def test_get_location_offset_increment():
    """
    Verifies that explicit integer depth passes through the tool helper
    with the +1 offset adjustment to maintain frame accuracy.
    """
    # Pokud zadáme get_location=1, helper by měl interně volat SimpleException(get_location=2)
    with pytest.raises(SimpleException) as exc:
        bool_or_exception(False, get_location=1)

    assert exc.value.get_location == 2


def test_oneline_flag_propagation():
    """Confirms that layout directives like oneline are passed through to the engine."""
    with pytest.raises(SimpleException) as exc:
        bool_or_exception(False, oneline=True)

    assert exc.value.oneline is True