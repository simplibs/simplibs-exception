import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.raise_system_blacklist_mutation_error import (
    raise_system_blacklist_mutation_error,
)


def test_always_raises_settings_error():
    with pytest.raises(SimpleExceptionSettingsError):
        raise_system_blacklist_mutation_error(("some", "value"))


def test_error_carries_the_offending_value():
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_system_blacklist_mutation_error("bad-value")

    assert exc_info.value.value == "bad-value"


def test_error_mentions_location_blacklist_as_the_alternative():
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_system_blacklist_mutation_error("x")

    how_to_fix = exc_info.value.how_to_fix
    joined = how_to_fix if isinstance(how_to_fix, str) else " ".join(how_to_fix)
    assert "LOCATION_BLACKLIST" in joined
