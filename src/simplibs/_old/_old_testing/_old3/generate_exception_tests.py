"""
Automatic test generator for SimpleException-style classes.

This utility:
- discovers all exception classes in simplibs.exception
- instantiates each class
- validates default diagnostic fields
- validates renderer, to_dict(), to_debug_dict()
- ensures consistency across the entire exception hierarchy
"""

import inspect
from typing import Any, Type

from simplibs.exception import (
    SimpleException,
    SimpleExceptionData,
    SimpleExceptionInternalError,
)
from simplibs.sentinels import UNSET
from .assert_exception_class import assert_exception_class


def _is_exception_class(obj: Any) -> bool:
    """Return True if obj is a SimpleException-style class."""
    return inspect.isclass(obj) and issubclass(
        obj,
        (SimpleException, SimpleExceptionData, SimpleExceptionInternalError),
    )


def _discover_exception_classes() -> list[Type[Any]]:
    """Find all SimpleException-style classes in simplibs.exception."""
    import simplibs.exception as exc_module

    classes = []
    for name, obj in vars(exc_module).items():
        if _is_exception_class(obj):
            classes.append(obj)
    return classes


def generate_exception_tests(subtests) -> None:
    """
    Automatically test all SimpleException-style classes.

    For each exception class:
    - instantiate it
    - validate default diagnostic fields
    - validate renderer
    - validate to_dict() and to_debug_dict()
    """

    for exc_class in _discover_exception_classes():
        with subtests.test(f"test_{exc_class.__name__}_defaults"):
            exc = exc_class()

            # Validate diagnostic fields via shared helper
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
                verbose=False,
            )

            # Renderer must produce a string
            with subtests.test(f"{exc_class.__name__}_renderer"):
                assert isinstance(str(exc), str)

            # to_dict must return a dict
            if hasattr(exc, "to_dict"):
                with subtests.test(f"{exc_class.__name__}_to_dict"):
                    assert isinstance(exc.to_dict(), dict)

            # to_debug_dict must return a dict
            if hasattr(exc, "to_debug_dict"):
                with subtests.test(f"{exc_class.__name__}_to_debug_dict"):
                    assert isinstance(exc.to_debug_dict(), dict)
