import pytest

from simplibs.exception._core_logic.lifecycle.new_method.add_exception_type import (
    add_exception_type,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


class PlainClsNoDefault:
    """A baseline host class with no 'exception' class attribute defined at all."""


class ClsWithNoneDefault:
    """Mirrors the real dataclass default where the 'exception' attribute is explicitly None."""
    exception = None


class MyCustomException(Exception):
    """A dummy custom exception used for ancestry evaluation."""


class ClsAlreadySubclassing(MyCustomException):
    """A host class that already includes MyCustomException in its static ancestry tree."""


def test_dynamic_class_is_created_and_cached_for_new_combination():
    """
    Verifies that a brand new combination of host class and foreign exception
    triggers the generation of a dynamic subclass, and that this new type
    is properly cataloged in the internal global memory cache.
    """
    class Base:
        pass

    class SomeException(Exception):
        pass

    # 1. Resolve the runtime class using the factory helper
    runtime_cls = add_exception_type(Base, exception=SomeException)

    # 2. Assert correct multi-inheritance graph resolution
    assert runtime_cls is not Base
    assert issubclass(runtime_cls, Base)
    assert issubclass(runtime_cls, SomeException)

    # 3. Assert registry state storage injection
    assert (Base, SomeException) in SimpleExceptionSettings._dynamic_cls_cache


def test_dynamic_class_is_reused_from_cache_on_second_call():
    """
    Guarantees that requesting the exact same combination of host class and
    foreign exception bypasses expensive type generation and reuses the previously
    compiled dynamic type blueprint from the performance cache.
    """
    class Base:
        pass

    class SomeException(Exception):
        pass

    # 1. Spawn the dynamic class representation twice
    first = add_exception_type(Base, exception=SomeException)
    second = add_exception_type(Base, exception=SomeException)

    # 2. Assert absolute structural identity to prove caching efficiency
    assert first is second


def test_exception_instance_is_normalized_to_its_type():
    """
    Ensures that if an external consumer accidentally passes an instantiated
    exception object instead of a class blueprint, the engine defensively flattens
    it to its root type and constructs the inheritance tree correctly.
    """
    class Base:
        pass

    class SomeException(Exception):
        pass

    # 1. Execute the factory, feeding an active exception instance
    runtime_cls = add_exception_type(Base, exception=SomeException("boom"))

    # 2. Validate that the root type was extracted and embedded
    assert issubclass(runtime_cls, Base)
    assert issubclass(runtime_cls, SomeException)


def test_no_exception_requested_and_no_class_default_returns_original_class():
    """
    Validates the empty fallback pathway: if no override parameter is supplied
    and the host class does not define a default attribute, the factory short-circuits
    and returns the original class blueprint completely untouched.
    """
    runtime_cls = add_exception_type(PlainClsNoDefault)
    assert runtime_cls is PlainClsNoDefault


def test_class_level_none_default_returns_original_class():
    """
    Verifies that a class-level default set explicitly to None is correctly resolved
    as a directive to skip dynamic inheritance, forcing the factory to return the
    original host blueprint unchanged.
    """
    runtime_cls = add_exception_type(ClsWithNoneDefault)
    assert runtime_cls is ClsWithNoneDefault


def test_already_subclassing_the_exception_returns_original_class():
    """
    Checks the circular redundancy shield: if the target host class already includes
    the requested exception type in its MRO graph, creating a dynamic type is redundant.
    The factory must return the original class to prevent graph corruption.
    """
    runtime_cls = add_exception_type(ClsAlreadySubclassing, exception=MyCustomException)
    assert runtime_cls is ClsAlreadySubclassing


def test_dynamic_class_mirrors_the_name_of_the_original_host_class():
    """
    Architectural Contract: Verifies that the factory injection process preserves
    the exact string name (__name__) of the original host class, ensuring that
    tracebacks, logger outputs, and debuggers remain intuitive.
    """

    class MySpecificDatabaseError(Exception):
        pass

    class TargetedHostBlueprint:
        pass

    runtime_cls = add_exception_type(TargetedHostBlueprint, exception=MySpecificDatabaseError)

    # The dynamically spawned class must inherit the semantic name signature exactly
    assert runtime_cls.__name__ == "TargetedHostBlueprint"