from simplibs.exception._core_logic.lifecycle.init_utils.normalize_string import (
    normalize_string,
)


class Dummy:
    label = "default-label"


def test_valid_string_is_passed_through():
    instance = Dummy()
    assert normalize_string(instance, "custom-label", "label") == "custom-label"


def test_empty_string_is_passed_through_as_is():
    # An empty string IS a str, so isinstance check passes; it is not
    # replaced by the class default.
    instance = Dummy()
    assert normalize_string(instance, "", "label") == ""


def test_invalid_value_falls_back_to_class_default():
    instance = Dummy()
    assert normalize_string(instance, 123, "label") == "default-label"


def test_none_falls_back_to_class_default():
    instance = Dummy()
    assert normalize_string(instance, None, "label") == "default-label"


def test_invalid_value_falls_back_to_none_when_no_class_default():
    class NoDefault:
        pass

    instance = NoDefault()
    assert normalize_string(instance, 123, "label") is None
