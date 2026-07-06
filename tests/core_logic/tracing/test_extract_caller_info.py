from simplibs.exception._core_logic.tracing.extract_caller_info import (
    extract_caller_info,
)
from _helper_wrapper import call_extract_caller_info


def test_basic_extraction_returns_immediate_caller():
    def entry_point():
        return extract_caller_info(expected_frames=1)

    info = entry_point()

    assert info is not None
    assert info["function"] == "entry_point"
    assert info["line"] > 0
    assert info["file"].endswith(".py")


def test_returns_dict_with_expected_keys():
    def entry_point():
        return extract_caller_info(expected_frames=1)

    info = entry_point()

    assert set(info.keys()) == {"file", "path", "line", "function"}


def test_filtering_via_excluded_patterns_skips_matching_file():
    """
    excluded_patterns matches against the FILE PATH of each frame, not the
    function name. Since call_extract_caller_info() lives in its own module
    (_helper_wrapper.py), excluding that filename correctly skips past it
    and lands on this test file/function instead.
    """

    def entry_point():
        return call_extract_caller_info(
            expected_frames=1,
            excluded_patterns=("_helper_wrapper.py",),
        )

    info = entry_point()

    assert info["function"] == "entry_point"


def test_without_excluded_patterns_returns_the_nearest_wrapper_frame():
    def entry_point():
        return call_extract_caller_info(expected_frames=1)

    info = entry_point()

    # No exclusion -> the nearest frame is inside the helper wrapper itself.
    assert info["function"] == "call_extract_caller_info"


def test_expected_frames_beyond_stack_depth_falls_back_to_outermost_frame():
    def entry_point():
        return extract_caller_info(expected_frames=999_999)

    info = entry_point()

    # Even when the requested depth is never reached, the function degrades
    # gracefully to the last frame walked instead of returning None.
    assert info is not None


def test_empty_stack_case_returns_none_is_not_triggered_in_practice():
    # `inspect.stack()` is never empty in a normal running interpreter, so
    # this documents the expectation rather than forcing that edge case.
    info = extract_caller_info(expected_frames=1)
    assert info is not None
