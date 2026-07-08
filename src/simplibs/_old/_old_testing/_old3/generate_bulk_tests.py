"""
Bulk test generator for SimpleException ecosystem.

This module allows you to define a list of items (exception classes,
raise-functions, validation functions) and automatically test them.

Supported item formats:

1) Exception class:
   SimpleExceptionSettingsError

2) Raise function (no parameters):
   (SimpleExceptionSettingsError, raise_settings_error)

3) Validation / logic function (with parameters):
   (SimpleExceptionSettingsError, validate_dynamic_cls_cache, "abc")
   (SimpleExceptionSettingsError, validate_user, 123, mode="strict")

The goal:
- Exception classes are tested deeply (instantiation, renderer, dicts).
- Functions are tested only for correct exception type.
- Verbose mode uses subtests for each item.
- Silent mode produces one aggregated PASS per item.
"""

from typing import Any, Callable, Type
import pytest

from simplibs.sentinels import UNSET
from .assert_exception_class import assert_exception_class
from .assert_exception_function import assert_exception_function
from .helpers.maybe_subtest import maybe_subtest


# ---------------------------------------------------------------------------
# 1) Helpers for item type detection
# ---------------------------------------------------------------------------

def _is_exception_class(item: Any) -> bool:
    """Return True if item is a SimpleException-style class."""
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
# 2) Bulk test generator
# ---------------------------------------------------------------------------

def generate_bulk_tests(
    subtests,
    items: list[Any],
    *,
    verbose: bool = True,
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

    Behavior
    --------
    - Exception classes are tested deeply via assert_exception_class().
    - Raise functions are tested only for correct exception type.
    - Validation functions are tested only for correct exception type.
    """

    for item in items:

        # ------------------------------
        # 1) Exception class
        # ------------------------------
        if _is_exception_class(item):
            exc_class = item
            name = f"exception_class::{exc_class.__name__}"

            with maybe_subtest(subtests, name, verbose):
                # Deep test of class defaults
                assert_exception_class(
                    subtests,
                    exc_class,
                    verbose=verbose,
                )
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


"""
# ⭐ Jak se to používá?

## 📌 1) Vytvoříš si seznam položek

```python
from simplibs.exception import (
    SimpleExceptionInternalError,
    SimpleExceptionModeError,
    SimpleExceptionSettingsError,
)

from myproject.exceptions import (
    raise_settings_error,
    validate_dynamic_cls_cache,
    validate_user,
)

ITEMS = [
    # 1) Definiční třídy výjimek
    SimpleExceptionInternalError,
    SimpleExceptionModeError,
    SimpleExceptionSettingsError,

    # 2) Raise funkce bez parametrů
    (SimpleExceptionSettingsError, raise_settings_error),

    # 3) Validační funkce s parametry
    (SimpleExceptionSettingsError, validate_dynamic_cls_cache, "abc"),
    (SimpleExceptionModeError, validate_user, 123, "strict"),
]
```

---

## 📌 2) V testu zavoláš generátor

```python
from simplibs.exception.testing.generate_bulk_tests import generate_bulk_tests

def test_bulk(subtests):
    generate_bulk_tests(subtests, ITEMS, verbose=True)
```

"""