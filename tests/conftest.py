import pytest

from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


@pytest.fixture(autouse=True)
def _reset_settings():
    """
    Ensures every test starts and ends with factory-default global settings.

    SimpleExceptionSettings is a shared, mutable, class-level singleton, so any
    test that mutates it (GET_LOCATION, LOCATION_BLACKLIST, MESSAGE_MODE, ...)
    could otherwise leak state into unrelated tests.
    """
    SimpleExceptionSettings.reset()
    yield
    SimpleExceptionSettings.reset()
