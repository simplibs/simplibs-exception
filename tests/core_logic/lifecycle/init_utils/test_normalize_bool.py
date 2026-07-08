from simplibs.exception._core_logic.lifecycle.init_utils.normalize_bool import (
    normalize_bool,
)


class Dummy:
    """Mock container defining a class-level fallback default for boolean configuration tests."""
    oneline = True


def test_valid_bool_true_is_passed_through():
    """Ensures that a valid raw True boolean is passed through completely un-mutated."""
    instance = Dummy()
    assert normalize_bool(instance, True, "oneline") is True


def test_valid_bool_false_is_passed_through():
    """Ensures that a valid raw False boolean is passed through completely un-mutated."""
    instance = Dummy()
    assert normalize_bool(instance, False, "oneline") is False


def test_invalid_value_falls_back_to_class_default():
    """Validates that supplying an invalid data type triggers a silent fallback to the class schema configuration."""
    instance = Dummy()
    assert normalize_bool(instance, "not-a-bool", "oneline") is True


def test_invalid_value_falls_back_to_false_when_no_class_default_defined():
    """
    Verifies defensive emergency mitigation: if an invalid type is passed and the class
    completely lacks the specified attribute fallback, the engine safe-guards execution by defaulting to False.
    """
    class NoDefault:
        pass

    instance = NoDefault()
    assert normalize_bool(instance, "nope", "oneline") is False


def test_none_value_falls_back_to_class_default():
    """Confirms that explicit None states are treated as unconfigured parameters, reverting to the class default."""
    instance = Dummy()
    assert normalize_bool(instance, None, "oneline") is True


def test_malformed_class_default_is_explicitly_casted_to_bool():
    """
    Architectural Edge Case: Verifies ultimate defensive mitigation logic. If the class-level
    default is itself corrupted (e.g., a truthy string instead of a strict bool), the engine
    must forcefully cast it into a primitive boolean state to guarantee layout type-safety.
    """

    class CorruptedDefault:
        oneline = "truthy-malformed-string"

    instance = CorruptedDefault()

    # Reverting to class default with an invalid parameter value must yield a clean boolean True
    assert normalize_bool(instance, None, "oneline") is True