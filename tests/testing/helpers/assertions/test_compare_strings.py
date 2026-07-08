"""
Tests for compare_strings — exact matching, fuzzy substring inclusion, and sequence flattening.
"""
import pytest
from simplibs.exception.testing._helpers.assertions.compare_strings import compare_strings


# -----------------------------------------------------------------------------
# Absolute Equality Mode (exact_match=True)
# -----------------------------------------------------------------------------

def test_exact_match_success():
    """Verify that exact_match=True passes on identical strings or tuples."""
    # Strings
    compare_strings("exact_text", "exact_text", exact_match=True)
    # Tuples
    compare_strings(("a", "b"), ("a", "b"), exact_match=True)
    # None values
    compare_strings(None, None, exact_match=True)


def test_exact_match_raises_assertion_error_on_mismatch():
    """Verify that exact_match=True strictly fails even on partial substring matches."""
    with pytest.raises(AssertionError):
        compare_strings("apple", "apple pie", exact_match=True)


# -----------------------------------------------------------------------------
# Fuzzy Substring Mode (exact_match=False)
# -----------------------------------------------------------------------------

def test_fuzzy_match_substring_success():
    """Verify that exact_match=False passes when test_value is a substring of exc_value."""
    compare_strings("apple", "apple pie", exact_match=False)
    compare_strings("pie", "apple pie", exact_match=False)


def test_fuzzy_match_raises_assertion_error_if_not_contained():
    """Verify that exact_match=False fails if the substring is completely missing."""
    with pytest.raises(AssertionError):
        compare_strings("banana", "apple pie", exact_match=False)


# -----------------------------------------------------------------------------
# Container Normalization & None Boundaries
# -----------------------------------------------------------------------------

def test_fuzzy_match_flattens_sequences():
    """Verify that sequence tuples are aggregated via spaces before fuzzy evaluation."""
    # test_value as tuple flattened into "error context" and looked up inside exc_value
    compare_strings(("error", "context"), "this is an error context block", exact_match=False)

    # exc_value as tuple flattened into "main issue details" and matched against test_value
    compare_strings("issue", ("main", "issue", "details"), exact_match=False)


def test_fuzzy_match_handles_none_safely():
    """Verify that None values evaluate gracefully as empty strings in fuzzy mode."""
    # Both None -> "" in "" -> True
    compare_strings(None, None, exact_match=False)

    # None in existing string -> "" in "something" -> True
    compare_strings(None, "something", exact_match=False)

    # Existing string in None -> "something" in "" -> False
    with pytest.raises(AssertionError):
        compare_strings("something", None, exact_match=False)