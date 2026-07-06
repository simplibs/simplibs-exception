from simplibs.exception._core_logic.lifecycle.init_utils.process_skip_locations import (
    process_skip_locations,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


class Dummy:
    skip_locations = ()


def test_merges_local_value_with_global_and_system_blacklists():
    instance = Dummy()
    result = process_skip_locations(instance, ("my_wrapper.py",))

    assert result[0] == "my_wrapper.py"
    for item in SimpleExceptionSettings.LOCATION_BLACKLIST:
        assert item in result
    for item in SimpleExceptionSettings._SYSTEM_BLACKLIST:
        assert item in result


def test_string_input_is_normalized_before_merging():
    instance = Dummy()
    result = process_skip_locations(instance, "single_pattern.py")

    assert result[0] == "single_pattern.py"


def test_none_input_still_includes_system_blacklist():
    instance = Dummy()
    result = process_skip_locations(instance, None)

    for item in SimpleExceptionSettings._SYSTEM_BLACKLIST:
        assert item in result


def test_result_is_always_a_tuple():
    instance = Dummy()
    result = process_skip_locations(instance, ["a.py", "b.py"])
    assert isinstance(result, tuple)
    assert "a.py" in result
    assert "b.py" in result


def test_reflects_updated_location_blacklist_setting():
    SimpleExceptionSettings.LOCATION_BLACKLIST = ("custom_blacklisted.py",)
    instance = Dummy()
    result = process_skip_locations(instance, None)
    assert "custom_blacklisted.py" in result
