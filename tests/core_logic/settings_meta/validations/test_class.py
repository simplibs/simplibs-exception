import pytest

from simplibs.exception._core_logic.internal_exceptions import (
    SimpleExceptionInternalError,
    SimpleExceptionModeError,
    SimpleExceptionSettingsError
)

from simplibs.exception.testing.__new.assert_class import (
    assert_exception_class_inheritance,
    assert_exception_class_interface,
    assert_exception_class_constructor,
    assert_exception_class_defaults
)
from simplibs.exception.testing.__new.assert_exception_class import assert_exception_class


def test_class(subtests):

    assert_exception_class(
        subtests, SimpleExceptionInternalError
    )

    # assert_exception_class_inheritance(
    #     subtests, SimpleExceptionInternalError
    # )
    #
    # assert_exception_class_defaults(
    #     subtests, SimpleExceptionInternalError
    # )
    #
    # assert_exception_class_constructor(
    #     subtests, SimpleExceptionInternalError
    # )
    #
    # assert_exception_class_interface(
    #     subtests, SimpleExceptionInternalError
    # )

