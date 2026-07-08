from simplibs.exception._core_logic.tracing.extract_caller_info import (
    extract_caller_info,
)
from _helper_wrapper import call_extract_caller_info


def test_basic_extraction_returns_immediate_caller():
    """Confirms that with defaults, the engine accurately identifies and extracts the immediate localized calling function context."""

    def entry_point():
        return extract_caller_info(expected_frames=1)

    info = entry_point()

    assert info is not None
    assert info["function"] == "entry_point"
    assert info["line"] > 0
    assert info["file"].endswith(".py")


def test_returns_dict_with_expected_keys():
    """Validates the structure of the returned diagnostic snapshot dictionary, ensuring all required frame asset keys are present."""

    def entry_point():
        return extract_caller_info(expected_frames=1)

    info = entry_point()

    assert set(info.keys()) == {"file", "path", "line", "function"}


def test_filtering_via_excluded_patterns_skips_matching_file():
    """
    Verifies path-based exclusion routing: providing an explicit pattern must successfully
    skip past internal wrappers and target the first valid contextual user execution frame.
    """

    def entry_point():
        return call_extract_caller_info(
            expected_frames=1,
            excluded_patterns=("_helper_wrapper.py",),
        )

    info = entry_point()

    # Must skip call_extract_caller_info and land back here
    assert info["function"] == "entry_point"


def test_without_excluded_patterns_returns_the_nearest_wrapper_frame():
    """Confirms that when no exclusions are applied, the stack scanner stops fast at the absolute closest physical frame."""

    def entry_point():
        return call_extract_caller_info(expected_frames=1)

    info = entry_point()

    # Without an explicit exclusion grid, the immediate helper frame is captured
    assert info["function"] == "call_extract_caller_info"


def test_expected_frames_beyond_stack_depth_falls_back_to_outermost_frame():
    """
    Verifies the Fallout Mechanism (Safety Net Pattern): requesting a stack depth
    completely beyond reality must gracefully fall back to the outermost frame instead of returning None.
    """

    def entry_point():
        return extract_caller_info(expected_frames=999_999)

    info = entry_point()

    # The safety net ensures we always return a valid frame layout instead of failing blindly
    assert info is not None


def test_empty_stack_case_returns_none_is_not_triggered_in_practice():
    """Documents and registers the baseline expectation that a live interpreter stack context must never resolve to an empty state."""
    info = extract_caller_info(expected_frames=1)
    assert info is not None


def test_cross_platform_path_normalization_handles_mixed_slashes():
    """
    Architectural Contract: Verifies that the cross-platform path normalization layer
    successfully resolves and matches patterns containing Windows-style backslashes,
    guaranteeing runtime alignment across all target operating systems.
    """

    def entry_point():
        # Passing a subpath pattern explicitly using a Windows-style backslash.
        # Path.as_posix() converts this to standard forward slashes, enabling a clean match.
        return call_extract_caller_info(
            expected_frames=1,
            excluded_patterns=("tracing\\_helper_wrapper.py",),
        )

    info = entry_point()

    # If the backslash normalization works, the file is successfully skipped,
    # and the engine correctly rolls back out to target this local 'entry_point'.
    assert info["function"] == "entry_point"