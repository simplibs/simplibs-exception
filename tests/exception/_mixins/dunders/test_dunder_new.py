"""
Tests for DunderNewMixin — exception resolution, dynamic class creation, and caching.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.exception._mixins.dunders.New import DunderNewMixin
from simplibs.exception.settings import SimpleExceptionSettings as S


# -----------------------------------------------------------------------------
# Test base class
# -----------------------------------------------------------------------------

class MockBase(DunderNewMixin):
    exception = UNSET

    def __init__(self, *args, **kwargs):
        pass


@pytest.fixture(autouse=True)
def clean_cache():
    """Clean cache before each test."""
    S.reset()
    yield
    S.reset()


# -----------------------------------------------------------------------------
# Step 2 — no exception
# -----------------------------------------------------------------------------

def test_without_exception_returns_original_class():
    """If no exception is provided, an instance of the original class must be returned."""
    instance = MockBase()
    assert type(instance) is MockBase
    assert not isinstance(instance, ValueError)


# -----------------------------------------------------------------------------
# Step 1 — class-level default
# -----------------------------------------------------------------------------

def test_class_default_exception_is_used():
    """An exception defined on the class must be used if none was passed as a parameter."""
    class TypeErrorBase(MockBase):
        exception = TypeError

    instance = TypeErrorBase()
    assert isinstance(instance, TypeError)
    assert isinstance(instance, TypeErrorBase)


# -----------------------------------------------------------------------------
# Step 3 — instance instead of class
# -----------------------------------------------------------------------------

def test_exception_instance_is_converted_to_type():
    """Passing an exception instance instead of a class must be silently converted to its type."""
    instance = MockBase(exception=RuntimeError())
    assert isinstance(instance, RuntimeError)
    assert type(instance) is not RuntimeError


# -----------------------------------------------------------------------------
# Step 4 — class already contains the exception
# -----------------------------------------------------------------------------

def test_already_subclass_returns_original_without_caching():
    """If the class already has the exception in its ancestors, no dynamic class must be created."""
    class AlreadyValue(MockBase, ValueError):
        pass

    instance = AlreadyValue(exception=ValueError)
    assert type(instance) is AlreadyValue
    assert (AlreadyValue, ValueError) not in S._dynamic_cls_cache


# -----------------------------------------------------------------------------
# Steps 5 & 6 — dynamic class and cache
# -----------------------------------------------------------------------------

def test_dynamic_class_has_both_base_and_exception():
    """The dynamic class must be an instance of both MockBase and the provided exception."""
    instance = MockBase(exception=ValueError)
    assert isinstance(instance, MockBase)
    assert isinstance(instance, ValueError)
    assert type(instance) is not MockBase


def test_dynamic_class_preserves_original_name():
    """The dynamic class must retain the same __name__ as the original class."""
    instance = MockBase(exception=ValueError)
    assert type(instance).__name__ == "MockBase"


def test_same_combination_returns_cached_class():
    """The same (class, exception) combination must return the identical class from cache."""
    instance1 = MockBase(exception=LookupError)
    instance2 = MockBase(exception=LookupError)
    assert type(instance1) is type(instance2)
    assert (MockBase, LookupError) in S._dynamic_cls_cache


def test_different_exceptions_create_separate_cache_entries():
    """Different exceptions must create separate cache entries."""
    MockBase(exception=ValueError)
    MockBase(exception=TypeError)
    assert (MockBase, ValueError) in S._dynamic_cls_cache
    assert (MockBase, TypeError) in S._dynamic_cls_cache