from simplibs.exception._core_logic.lifecycle.init_utils.normalize_bool import (
    normalize_bool,
)


class Dummy:
    oneline = True  # class-level default used as fallback


def test_valid_bool_true_is_passed_through():
    instance = Dummy()
    assert normalize_bool(instance, True, "oneline") is True


def test_valid_bool_false_is_passed_through():
    instance = Dummy()
    assert normalize_bool(instance, False, "oneline") is False


def test_invalid_value_falls_back_to_class_default():
    instance = Dummy()
    assert normalize_bool(instance, "not-a-bool", "oneline") is True


def test_invalid_value_falls_back_to_false_when_no_class_default_defined():
    class NoDefault:
        pass

    instance = NoDefault()
    assert normalize_bool(instance, "nope", "oneline") is False


def test_none_value_falls_back_to_class_default():
    instance = Dummy()
    assert normalize_bool(instance, None, "oneline") is True
