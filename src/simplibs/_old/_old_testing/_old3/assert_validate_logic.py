"""
Bulk test generator for SimpleException ecosystem.

Supports two modes:
- shallow mode (default): only checks that the correct exception is raised
- deep mode: performs full SimpleException-style validation of exception classes

Supported item formats:

1) Exception class:
   SimpleExceptionSettingsError

2) Raise function (no parameters):
   (SimpleExceptionSettingsError, raise_settings_error)

3) Validation / logic function (with parameters):
   (SimpleExceptionSettingsError, validate_dynamic_cls_cache, "abc")
   (SimpleExceptionSettingsError, validate_user, 123, mode="strict")

Deep mode:
- verifies subclassing of SimpleExceptionData
- verifies instantiation
- verifies default diagnostic fields
- verifies renderer
- verifies to_dict() and to_debug_dict()
"""

from typing import Any, Callable, Type
import pytest

from simplibs.sentinels import UNSET
from simplibs.exception import SimpleExceptionData
from .assert_exception_class import assert_exception_class
from .helpers.maybe_subtest import maybe_subtest


# ---------------------------------------------------------------------------
# 1) Helpers for item type detection
# ---------------------------------------------------------------------------

def is_exception_class(item: Any) -> bool:
    """Return True if item is a BaseException subclass."""
    return isinstance(item, type) and issubclass(item, BaseException)


def _is_raise_function(item: Any) -> bool:
    """
    Return True if item is a tuple of:
        (exception_class, function)
    where function takes no parameters.
    """
    if not isinstance(item, tuple):
        return False
    if len(item) != 2:
        return False

    exc_class, func = item
    return (
        isinstance(exc_class, type)
        and issubclass(exc_class, BaseException)
        and callable(func)
    )


def _is_validation_function(item: Any) -> bool:
    """
    Return True if item is a tuple of:
        (exception_class, function, *params)
    where params are passed to the function.
    """
    if not isinstance(item, tuple):
        return False
    if len(item) < 3:
        return False

    exc_class, func = item[0], item[1]
    return (
        isinstance(exc_class, type)
        and issubclass(exc_class, BaseException)
        and callable(func)
    )


# ---------------------------------------------------------------------------
# 2) Deep mode logic for SimpleException-style classes
# ---------------------------------------------------------------------------

def _deep_test_exception_class(subtests, exc_class: Type[Any], verbose: bool) -> None:
    """
    Perform full SimpleException-style validation:
    - subclassing check
    - instantiation
    - default diagnostic fields
    - renderer
    - to_dict()
    - to_debug_dict()
    """

    name = f"deep_exception_class::{exc_class.__name__}"

    with maybe_subtest(subtests, name, verbose):
        # 1) Must be subclass of SimpleExceptionData
        assert issubclass(exc_class, SimpleExceptionData), (
            f"{exc_class.__name__} is not a subclass of SimpleExceptionData"
        )

        # 2) Instantiate
        exc = exc_class()

        # 3) Validate default diagnostic fields
        assert_exception_class(
            subtests,
            exc_class,
            error_name=getattr(exc, "error_name", UNSET),
            label=getattr(exc, "label", UNSET),
            expected=getattr(exc, "expected", UNSET),
            value=getattr(exc, "value", UNSET),
            problem=getattr(exc, "problem", UNSET),
            context=getattr(exc, "context", UNSET),
            how_to_fix=getattr(exc, "how_to_fix", UNSET),
            exception=getattr(exc, "exception", UNSET),
            get_location=getattr(exc, "get_location", UNSET),
            skip_locations=getattr(exc, "skip_locations", UNSET),
            oneline=getattr(exc, "oneline", UNSET),
            verbose=verbose,
        )

        # 4) Renderer must produce a string
        with maybe_subtest(subtests, f"{exc_class.__name__}_renderer", verbose):
            assert isinstance(str(exc), str)

        # 5) to_dict must return a dict
        if hasattr(exc, "to_dict"):
            with maybe_subtest(subtests, f"{exc_class.__name__}_to_dict", verbose):
                assert isinstance(exc.to_dict(), dict)

        # 6) to_debug_dict must return a dict
        if hasattr(exc, "to_debug_dict"):
            with maybe_subtest(subtests, f"{exc_class.__name__}_to_debug_dict", verbose):
                assert isinstance(exc.to_debug_dict(), dict)


# ---------------------------------------------------------------------------
# 3) Bulk test generator
# ---------------------------------------------------------------------------

def generate_bulk_tests(
    subtests,
    items: list[Any],
    *,
    verbose: bool = True,
    deep_exception_check: bool = False,
) -> None:
    """
    Bulk test generator.

    Parameters
    ----------
    subtests : pytest subtests fixture
    items : list[Any]
        List of items to test. Each item can be:
        - exception class
        - (exception_class, raise_function)
        - (exception_class, validation_function, *params)
    verbose : bool
        If True → each item uses its own subtest.
        If False → only one PASS per item.
    deep_exception_check : bool
        If True → exception classes are validated deeply (SimpleException-style).
        If False → only shallow instantiation check is performed.
    """

    for item in items:

        # ------------------------------
        # 1) Exception class
        # ------------------------------
        if _is_exception_class(item):
            exc_class = item

            if deep_exception_check:
                _deep_test_exception_class(subtests, exc_class, verbose)
            else:
                name = f"exception_class::{exc_class.__name__}"
                with maybe_subtest(subtests, name, verbose):
                    # Shallow check: must instantiate
                    exc = exc_class()
                    assert isinstance(exc, exc_class)

            continue

        # ------------------------------
        # 2) Raise function (no params)
        # ------------------------------
        if _is_raise_function(item):
            exc_class, func = item
            name = f"raise_function::{func.__name__}"

            with maybe_subtest(subtests, name, verbose):
                with pytest.raises(exc_class):
                    func()
            continue

        # ------------------------------
        # 3) Validation function (with params)
        # ------------------------------
        if _is_validation_function(item):
            exc_class = item[0]
            func = item[1]
            params = item[2:]

            name = f"validation_function::{func.__name__}"

            with maybe_subtest(subtests, name, verbose):
                with pytest.raises(exc_class):
                    func(*params)
            continue

        # ------------------------------
        # 4) Unknown item type
        # ------------------------------
        with maybe_subtest(subtests, "unknown_item", verbose):
            raise AssertionError(
                f"Unsupported item format: {item!r}"
            )
