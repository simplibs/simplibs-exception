import pytest

from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception._core_logic.settings_meta.validations.raise_system_blacklist_mutation_error import (
    raise_system_blacklist_mutation_error,
)


def test_always_raises_settings_error():
    """Ensures that invoking the raiser consistently triggers a terminal SimpleExceptionSettingsError footprint."""
    with pytest.raises(SimpleExceptionSettingsError):
        raise_system_blacklist_mutation_error(("some", "value"))


def test_error_carries_the_offending_value():
    """Validates that the generated exception vehicle successfully carries the exact offending payload value for debugging."""
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_system_blacklist_mutation_error("bad-value")

    assert exc_info.value.value == "bad-value"


def test_error_mentions_location_blacklist_as_the_alternative():
    """
    Verifies UX and instructional quality: the raised error blueprint must explicitly
    point the user toward 'LOCATION_BLACKLIST' inside its remediation documentation.
    """
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_system_blacklist_mutation_error("x")

    how_to_fix = exc_info.value.how_to_fix
    joined = how_to_fix if isinstance(how_to_fix, str) else " ".join(how_to_fix)

    assert "LOCATION_BLACKLIST" in joined


def test_error_payload_contains_precise_diagnostic_metadata():
    """
    Architectural Contract: Verifies that the raised internal exception contains
    the exact structural diagnostic keys required by the terminal rendering engine.
    """
    with pytest.raises(SimpleExceptionSettingsError) as exc_info:
        raise_system_blacklist_mutation_error("any-payload")

    err = exc_info.value

    # Assert strict semantic assignment to secure visual rendering output layouts
    assert err.label == "SimpleExceptionSettings"
    assert "strict read-only metadata" in err.problem