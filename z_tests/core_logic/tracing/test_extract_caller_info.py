"""
Tests for extract_caller_info — stack walking, filtering, cross-platform normalization, and fallback safety.
"""
import os
import pytest
from simplibs.exception._core_logic.tracing.extract_caller_info import extract_caller_info


# -----------------------------------------------------------------------------
# Basic Extraction & Integrity
# -----------------------------------------------------------------------------

def test_extract_basic_current_frame():
    """Verify that calling the function without exclusions returns the immediate caller frame info."""

    def alpha_frame():
        return extract_caller_info(expected_frames=1)

    info = alpha_frame()

    assert isinstance(info, dict)
    assert info["function"] == "alpha_frame"
    assert info["file"] == "test_extract_caller_info.py"
    assert info["path"].endswith("test_extract_caller_info.py")
    assert isinstance(info["line"], int)


def test_extract_with_deeper_expected_frame():
    """Verify that changing expected_frames walks further up the active stack."""

    def target_frame():
        return intermediate_frame()

    def intermediate_frame():
        # expected_frames=2 should skip intermediate_frame and hit target_frame
        return extract_caller_info(expected_frames=2)

    info = target_frame()
    assert info["function"] == "target_frame"


# -----------------------------------------------------------------------------
# Filtering & Cross-Platform POSIX Normalization
# -----------------------------------------------------------------------------

def test_filtering_via_excluded_patterns():
    """Verify that frames matching excluded_patterns are dynamically skipped."""

    def entry_point():
        return blacklisted_layer()

    def blacklisted_layer():
        # We exclude 'blacklisted_layer' from the footprint. 
        # expected_frames=1 should skip this frame and return entry_point instead.
        return extract_caller_info(expected_frames=1, excluded_patterns=("blacklisted_layer",))

    info = entry_point()
    assert info["function"] == "entry_point"


def test_posix_path_normalization_matching():
    """Verify cross-platform matching by using forward slashes in patterns against any OS path."""

    def test_frame():
        # Simulating a pattern with a forward slash to ensure Path.as_posix() matches correctly
        current_dir = os.path.basename(os.path.dirname(__file__))
        pattern = f"{current_dir}/test_extract_caller_info"

        return extract_caller_info(expected_frames=2, excluded_patterns=(pattern,))

    # Skipping our own frame via the folder/file pattern should bubble up to pytest's runner frame
    info = test_frame()
    assert info["function"] != "test_frame"


# -----------------------------------------------------------------------------
# Fallout Mechanism (Safety Net Pattern)
# -----------------------------------------------------------------------------

def test_fallout_mechanism_returns_last_touched_frame():
    """If everything is blacklisted, the engine must return the last physically touched frame instead of None."""

    def worst_case_frame():
        # We exclude EVERYTHING, including common denominators or parts of this file
        return extract_caller_info(
            expected_frames=1,
            excluded_patterns=("test_extract_caller_info", "pytest", "py")
        )

    info = worst_case_frame()

    # The safety net should refuse to return None and give us the last frame it evaluated
    assert info is not None
    assert isinstance(info, dict)
    assert "file" in info
    assert "function" in info


# -----------------------------------------------------------------------------
# Zero-Crash Guarantee Directive
# -----------------------------------------------------------------------------

def test_zero_crash_guarantee_on_invalid_parameters():
    """Verify the 'Do no harm' directive — invalid types or broken internals return None, never crash."""
    # Passing incompatible types that would normally break sequence iteration or integer casting
    info_bad_frames = extract_caller_info(expected_frames="invalid_int_cast")  # type: ignore
    info_bad_patterns = extract_caller_info(excluded_patterns=12345)  # type: ignore

    assert info_bad_frames is None
    assert info_bad_patterns is None