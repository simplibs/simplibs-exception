import pytest

from simplibs.exception._core_logic.lifecycle.new_method.add_exception_type import (
    add_exception_type,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


class PlainClsNoDefault:
    """A class with no 'exception' class attribute defined at all."""


class ClsWithNoneDefault:
    """Mirrors the real dataclass default: 'exception' class attribute is None."""
    exception = None


class MyCustomException(Exception):
    pass


class ClsAlreadySubclassing(MyCustomException):
    """Already includes MyCustomException in its ancestry."""


def test_dynamic_class_is_created_and_cached_for_new_combination():
    class Base:
        pass

    class SomeException(Exception):
        pass

    instance = add_exception_type(Base, exception=SomeException)

    assert isinstance(instance, Base)
    assert isinstance(instance, SomeException)
    assert (Base, SomeException) in SimpleExceptionSettings._dynamic_cls_cache


def test_dynamic_class_is_reused_from_cache_on_second_call():
    class Base:
        pass

    class SomeException(Exception):
        pass

    first = add_exception_type(Base, exception=SomeException)
    second = add_exception_type(Base, exception=SomeException)

    assert type(first) is type(second)


def test_exception_instance_is_normalized_to_its_type():
    class Base:
        pass

    class SomeException(Exception):
        pass

    instance = add_exception_type(Base, exception=SomeException("boom"))

    assert isinstance(instance, SomeException)


def test_no_exception_requested_and_no_class_default_raises_due_to_bare_super_call():
    """
    KNOWN ISSUE: when `exception` resolves to UNSET (no override, no class-level
    default), add_exception_type falls back to `return super().__new__(cls)`.
    Because this is a bare, zero-argument `super()` call inside a plain
    module-level function (not textually defined inside a class body), Python
    cannot resolve the implicit __class__ cell, and this always raises a
    RuntimeError instead of returning a normal instance.
    """
    with pytest.raises(RuntimeError):
        add_exception_type(PlainClsNoDefault)  # exception defaults to UNSET


def test_class_level_none_default_raises_typeerror_on_issubclass_check():
    """
    KNOWN ISSUE: real subclasses of SimpleExceptionData default `exception` to
    None (not UNSET). add_exception_type only special-cases UNSET, so a class
    attribute of None slips past the first check and reaches
    `issubclass(cls, exception)` with exception=None, which raises TypeError.
    """
    with pytest.raises(TypeError):
        add_exception_type(ClsWithNoneDefault)  # exception defaults to UNSET


def test_already_subclassing_the_exception_raises_due_to_bare_super_call():
    """
    KNOWN ISSUE: same bare `super()` problem as above, reached via the
    "already included" short-circuit branch instead of the UNSET branch.
    """
    with pytest.raises(RuntimeError):
        add_exception_type(ClsAlreadySubclassing, exception=MyCustomException)
