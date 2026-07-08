from simplibs.exception._core_logic.lifecycle.init_utils.normalize_string import (
    normalize_string,
)


class Dummy:
    """Mock container providing a declarative class-level string fallback for validation testing."""
    label = "default-label"


def test_valid_string_is_passed_through():
    """Ensures that a valid raw string is passed through completely un-mutated."""
    instance = Dummy()
    assert normalize_string(instance, "custom-label", "label") == "custom-label"


def test_empty_string_is_passed_through_as_is():
    """
    Validates boundary behavior: an empty string is still a valid instance of 'str'
    and must be preserved as-is, preventing the engine from triggering a fallback cycle.
    """
    instance = Dummy()
    assert normalize_string(instance, "", "label") == ""


def test_invalid_value_falls_back_to_class_default():
    """Guarantees that supplying an invalid data type triggers a silent fallback to the class default configuration."""
    instance = Dummy()
    assert normalize_string(instance, 123, "label") == "default-label"


def test_none_falls_back_to_class_default():
    """Confirms that explicit None states are treated as unconfigured parameters, reverting to the class default."""
    instance = Dummy()
    assert normalize_string(instance, None, "label") == "default-label"


def test_invalid_value_falls_back_to_none_when_no_class_default():
    """
    Verifies defensive emergency handling: if an invalid type is passed and the class
    completely lacks the specified attribute fallback, the engine safely returns None.
    """
    class NoDefault:
        pass

    instance = NoDefault()
    assert normalize_string(instance, 123, "label") is None


def test_non_nullable_error_name_attribute_fallback():
    """
    Architectural Edge Case: Verifies fallback routing for strict non-nullable fields.
    Supplying an invalid type for a field like 'error_name' must resolve to the strict
    class-level string representation, safeguarding type-safety constraints.
    """

    class TargetExceptionMock:
        error_name = "ERROR"

    instance = TargetExceptionMock()

    # Passing an invalid integer must trigger a clean fallback to the default 'ERROR' string
    assert normalize_string(instance, 999, "error_name") == "ERROR"