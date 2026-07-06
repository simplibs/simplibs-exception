from simplibs.exception._core_logic.lifecycle.init_utils.normalize_exception import (
    normalize_exception,
)


class Dummy:
    exception = ValueError  # class-level default used as fallback


def test_exception_instance_is_returned_as_is():
    instance = Dummy()
    err = TypeError("boom")
    assert normalize_exception(instance, err, "exception") is err


def test_exception_class_is_returned_as_is():
    instance = Dummy()
    assert normalize_exception(instance, KeyError, "exception") is KeyError


def test_invalid_value_falls_back_to_class_default():
    instance = Dummy()
    assert normalize_exception(instance, "not-an-exception", "exception") is ValueError


def test_invalid_value_falls_back_to_none_when_no_class_default():
    class NoDefault:
        pass

    instance = NoDefault()
    assert normalize_exception(instance, 123, "exception") is None


def test_default_attr_name_is_exception():
    instance = Dummy()
    assert normalize_exception(instance, None) is ValueError
