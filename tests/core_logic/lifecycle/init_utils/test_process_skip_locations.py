from simplibs.exception._core_logic.lifecycle.init_utils.process_skip_locations import (
    process_skip_locations,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings


class Dummy:
    """Mock container defining a baseline fallback for skip_locations attributes."""
    skip_locations = ()


def test_merges_local_value_with_global_and_system_blacklists():
    """
    Ensures the compilation matrix builds correctly: local, global user, and core
    system blacklists must be merged sequentially in the precise order of intent.
    """
    # 1. Initialize data mock environment
    instance = Dummy()

    # 2. Execute compilation with a local override tuple
    result = process_skip_locations(instance, ("my_wrapper.py",))

    # 3. Assert correct array sequencing and inclusion
    assert result[0] == "my_wrapper.py"
    for item in SimpleExceptionSettings.LOCATION_BLACKLIST:
        assert item in result
    for item in SimpleExceptionSettings._SYSTEM_BLACKLIST:
        assert item in result


def test_string_input_is_normalized_before_merging():
    """Validates that a single raw string parameter is correctly encapsulated into a tuple before consolidation."""
    instance = Dummy()
    result = process_skip_locations(instance, "single_pattern.py")

    assert result[0] == "single_pattern.py"


def test_none_input_still_includes_system_blacklist():
    """Verifies that an unconfigured or empty input argument still seamlessly inherits the core infrastructure filters."""
    instance = Dummy()
    result = process_skip_locations(instance, None)

    for item in SimpleExceptionSettings._SYSTEM_BLACKLIST:
        assert item in result


def test_result_is_always_a_tuple():
    """Guarantees that regardless of the incoming container type (e.g., list), the output is locked as an immutable tuple."""
    instance = Dummy()
    result = process_skip_locations(instance, ["a.py", "b.py"])

    assert isinstance(result, tuple)
    assert "a.py" in result
    assert "b.py" in result


def test_reflects_updated_location_blacklist_setting():
    """
    Confirms runtime reactivity: dynamically updating SimpleExceptionSettings.LOCATION_BLACKLIST
    must instantly impact downstream compilation results.
    """
    # 1. Hot-swap the shared settings registry matrix state
    SimpleExceptionSettings.LOCATION_BLACKLIST = ("custom_blacklisted.py",)
    instance = Dummy()

    # 2. Compile blacklist pipeline
    result = process_skip_locations(instance, None)

    # 3. Verify the dynamic setting injected successfully
    assert "custom_blacklisted.py" in result


def test_strict_sequential_compilation_ordering():
    """
    Architectural Contract: Verifies the exact sequence indexing of the compiled array.
    To guarantee short-circuit trace performance, the array must strictly layout:
    [Local Patterns] -> [Global User Blacklist] -> [System Protected Frames].
    """
    # 1. Setup isolated mock values only for the mutable user blacklist
    SimpleExceptionSettings.LOCATION_BLACKLIST = ("user_global.py",)

    # 2. Extract the actual read-only system blacklist dynamically
    actual_system_core = SimpleExceptionSettings._SYSTEM_BLACKLIST

    instance = Dummy()
    local_input = ("local_override.py",)

    # 3. Run compilation pass
    result = process_skip_locations(instance, local_input)

    # 4. Assert precise sequential compilation order using the immutable system tuple
    expected_layout = ("local_override.py", "user_global.py") + actual_system_core
    assert result == expected_layout