"""
Tests for extract_caller_info — return keys, value types, expected_frames,
normalization, and fallout resilience.
"""
import pytest
import os
from pathlib import Path
from simplibs.exception.core._data_mixin.properties.utils.extract_caller_info import extract_caller_info


# -----------------------------------------------------------------------------
# Return keys and types
# -----------------------------------------------------------------------------

def test_returns_dict_with_correct_keys():
    """Result must contain exactly these keys: file, full_path, line, function."""
    result = extract_caller_info()
    assert result is not None
    assert set(result.keys()) == {"file", "full_path", "line", "function"}


def test_return_value_types():
    """line must be int, all other values must be str."""
    result = extract_caller_info()
    assert result is not None
    assert isinstance(result["line"], int)
    assert isinstance(result["file"], str)
    assert isinstance(result["full_path"], str)
    assert isinstance(result["function"], str)


# -----------------------------------------------------------------------------
# Value correctness & Normalization
# -----------------------------------------------------------------------------

def test_file_is_basename_of_full_path():
    """file must be the basename of full_path."""
    result = extract_caller_info()
    assert result is not None
    assert result["file"] == os.path.basename(result["full_path"])


def test_posix_normalization_in_matching():
    """Should match patterns even if they are provided with different slashes."""
    # Simulate pattern with POSIX slash, even if on Windows
    pattern = "tests/utils"
    # If normalization fails, this test might behave unpredictably on Windows
    result = extract_caller_info(excluded_patterns=(pattern,))

    # If a result is returned, it must not contain the pattern in the normalized path
    if result:
        normalized_path = Path(result["full_path"]).as_posix()
        assert pattern not in normalized_path


# -----------------------------------------------------------------------------
# expected_frames (1-based logic)
# -----------------------------------------------------------------------------

def test_expected_frames_one_points_to_direct_caller():
    """expected_frames=1 must point to the first non-excluded frame (the direct caller)."""
    def wrapper():
        return extract_caller_info(expected_frames=1)

    result = wrapper()
    assert result is not None
    assert result["function"] == "wrapper"


def test_expected_frames_two_points_to_caller_of_caller():
    """expected_frames=2 must return the second valid frame in the stack."""

    def level_2():
        return extract_caller_info(expected_frames=2)

    def level_1():
        # Stack here: level_2 -> level_1 -> test_func
        # level_2 is #1, level_1 is #2
        return level_2()

    result = level_1()
    assert result is not None
    assert result["function"] == "level_1"


# -----------------------------------------------------------------------------
# excluded_patterns & Fallout
# -----------------------------------------------------------------------------

def test_excluded_pattern_skips_matching_frames():
    """Frames whose path contains an excluded pattern must be skipped."""
    # Exclude the current file
    current_file_stem = Path(__file__).stem
    result = extract_caller_info(excluded_patterns=(current_file_stem,))

    # If fallout worked, we get the last frame (entry point),
    # otherwise we get a frame outside of this file.
    if result:
        assert current_file_stem not in result["file"]


def test_fallout_mechanism_when_all_excluded():
    """If everything is excluded, it must return the last available frame (fallout)."""
    # Exclude everything (slash is in every path)
    result = extract_caller_info(excluded_patterns=("/",))

    # Should not return None, but the last frame in the stack (e.g., from pytest or system)
    assert result is not None
    assert "file" in result


def test_fallout_when_expected_frames_out_of_bounds():
    """If expected_frames is too high, it must return the last available frame."""
    result = extract_caller_info(expected_frames=9999)

    # Instead of None (old behavior), we now expect a safety net (fallout)
    assert result is not None
    assert isinstance(result["line"], int)


# -----------------------------------------------------------------------------
# Resilience
# -----------------------------------------------------------------------------

def test_invalid_expected_frames_type_returns_fallout():
    """
    An invalid type shouldn't crash but will trigger the fallout mechanism
    because final_frame is set before the type error occurs.
    """
    result = extract_caller_info(expected_frames=None) # type: ignore
    assert result is not None
    assert "file" in result