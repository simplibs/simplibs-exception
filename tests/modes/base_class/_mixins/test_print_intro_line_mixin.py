"""
Tests for PrintIntroLineMixin — intro line formatting with and without value_label.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.core.data.SimpleExceptionData import SimpleExceptionData
from simplibs.exception.modes.base_class._mixins.PrintIntroLine import PrintIntroLineMixin


class MockMode(PrintIntroLineMixin):
    pass


@pytest.fixture
def mode():
    return MockMode()


# -----------------------------------------------------------------------------
# PrintIntroLineMixin
# -----------------------------------------------------------------------------

def test_with_value_label(mode):
    """Must return 'error_name: value_label' when value_label is set."""
    data = SimpleExceptionData(error_name="TEST_ERROR", value_label="my_param")
    assert mode._print_intro_line(data) == "⚠️ TEST_ERROR: my_param"


def test_without_value_label(mode):
    """Must return 'error_name:' when value_label is UNSET."""
    data = SimpleExceptionData(error_name="TEST_ERROR", value_label=UNSET)
    assert mode._print_intro_line(data) == "⚠️ TEST_ERROR:"


def test_default_value_label_is_unset(mode):
    """Default SimpleExceptionData (no value_label) must also return the format without a label."""
    data = SimpleExceptionData(error_name="TEST_ERROR")
    assert mode._print_intro_line(data) == "⚠️ TEST_ERROR:"