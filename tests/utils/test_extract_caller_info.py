"""
Tests for extract_caller_info — return keys, value types, skip_frames, excluded patterns, and failure resilience.
"""
import pytest
import os
from simplibs.exception.utils import extract_caller_info


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
# Value correctness
# -----------------------------------------------------------------------------

def test_file_is_basename_of_full_path():
    """file must be the basename of full_path."""
    result = extract_caller_info()
    assert result is not None
    assert result["file"] == os.path.basename(result["full_path"])


# -----------------------------------------------------------------------------
# skip_frames
# -----------------------------------------------------------------------------

def test_skip_frames_zero_points_to_direct_caller():
    """skip_frames=0 must point to the function that called extract_caller_info."""
    def wrapper():
        return extract_caller_info(skip_frames=0)

    result = wrapper()
    assert result is not None
    assert result["function"] == "wrapper"


def test_skip_frames_one_points_to_caller_of_caller():
    """skip_frames=1 must skip one extra frame above the direct caller."""
    def level_2():
        return extract_caller_info(skip_frames=1)

    def level_1():
        return level_2()

    result = level_1()
    assert result is not None
    assert result["function"] == "level_1"


# -----------------------------------------------------------------------------
# excluded_patterns
# -----------------------------------------------------------------------------

def test_excluded_pattern_skips_matching_frames():
    """Frames whose path contains an excluded pattern must be skipped."""
    current_file = "test_extract_caller_info"
    result = extract_caller_info(excluded_patterns=(current_file,))
    if result:
        assert current_file not in result["full_path"]


def test_always_excluded_skips_dynamic_frames():
    """Frames with '<' in their path (e.g. <string>) must always be skipped."""
    result = extract_caller_info()
    assert result is not None
    assert "<" not in result["full_path"]


# -----------------------------------------------------------------------------
# Failure resilience — returning None
# -----------------------------------------------------------------------------

def test_invalid_skip_frames_type_returns_none():
    """An invalid skip_frames type must be caught gracefully and return None."""
    assert extract_caller_info(skip_frames="invalid") is None


def test_too_large_skip_frames_returns_none():
    """A skip_frames value larger than the stack depth must return None."""
    assert extract_caller_info(skip_frames=99999) is None