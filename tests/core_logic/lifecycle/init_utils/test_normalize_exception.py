from simplibs.exception._core_logic.lifecycle.init_utils.normalize_exception import (
    normalize_exception,
)


class Dummy:
    """Mock baseline schema container providing a standard class-level exception type fallback."""
    exception = ValueError


def test_exception_instance_is_returned_as_is():
    """Ensures that a fully instantiated live exception object is accepted and returned un-mutated."""
    instance = Dummy()
    err = TypeError("boom")
    assert normalize_exception(instance, err, "exception") is err


def test_exception_class_is_returned_as_is():
    """Validates that a raw exception class type reference is processed and accepted correctly."""
    instance = Dummy()
    assert normalize_exception(instance, KeyError, "exception") is KeyError


def test_invalid_value_falls_back_to_class_default():
    """Guarantees that passing an entirely invalid data type triggers a silent fallback to the class default."""
    instance = Dummy()
    assert normalize_exception(instance, "not-an-exception", "exception") is ValueError


def test_invalid_value_falls_back_to_none_when_no_class_default():
    """
    Verifies defensive emergency handling: if an invalid payload is supplied and the class
    completely lacks a fallback attribute declaration, the engine safely returns None.
    """
    class NoDefault:
        pass

    instance = NoDefault()
    assert normalize_exception(instance, 123, "exception") is None


def test_default_attr_name_is_exception():
    """Confirms that the underlying string literal parameter default maps cleanly to the 'exception' key."""
    instance = Dummy()
    assert normalize_exception(instance, None) is ValueError


def test_non_exception_classes_and_raw_objects_safely_bypass_subclass_check():
    """
    Architectural Edge Case: Verifies the TypeError safety guard. Passing custom non-exception
    classes or raw instances must be intercepted early by the type inspector, preventing
    fatal built-in issubclass execution crashes and reverting cleanly to the registered fallback.
    """

    class RegularUserClass:
        pass

    instance = Dummy()

    # 1. Test passing a raw non-exception class type reference
    assert normalize_exception(instance, RegularUserClass, "exception") is ValueError

    # 2. Test passing an active instance of a non-exception class
    assert normalize_exception(instance, RegularUserClass(), "exception") is ValueError
