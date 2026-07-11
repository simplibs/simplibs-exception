"""
Tests for compare_strings — exact matching, fuzzy substring lookups, and sequence flattening.
"""
import pytest
from simplibs.sentinels import UNSET
from simplibs.exception.testing._helpers.compare_strings import compare_strings


# -----------------------------------------------------------------------------
# Exact Match Mode (exact_match=True)
# -----------------------------------------------------------------------------

def test_exact_match_success_on_identical_strings():
    """Verify that identical strings pass under strict equality mode."""
    compare_strings("Exact Message", "Exact Message", exact_match=True)


def test_exact_match_fails_on_partial_mismatch():
    """Verify that partial substrings fail when exact match is enforced."""
    with pytest.raises(AssertionError):
        compare_strings("Part", "Partial Message", exact_match=True)


def test_exact_match_success_on_identical_tuples():
    """Verify that identical tuple sequences pass under strict equality mode."""
    compare_strings(("line 1", "line 2"), ("line 1", "line 2"), exact_match=True)


# -----------------------------------------------------------------------------
# Fuzzy Substring Mode (exact_match=False)
# -----------------------------------------------------------------------------

def test_fuzzy_match_success_on_substring():
    """Verify that standard substring inclusion passes under fuzzy mode."""
    compare_strings("Target", "This is the Target message", exact_match=False)


def test_fuzzy_match_fails_if_substring_missing():
    """Verify that fuzzy mode fails if the expected token is completely missing."""
    with pytest.raises(AssertionError):
        compare_strings("Missing", "This is the Target message", exact_match=False)


def test_fuzzy_match_flattens_tuples_safely():
    """Verify that expected or actual tuples are flattened into strings and compared."""
    # Expected tuple is flattened to "line 1 line 2" -> should be found in actual string
    compare_strings(
        test_value=("line 1", "line 2"),
        exc_value="Error: line 1 line 2 occurred",
        exact_match=False
    )

    # Expected string found inside flattened actual tuple
    compare_strings(
        test_value="critical failure",
        exc_value=("System error:", "critical failure", "detected"),
        exact_match=False
    )


# -----------------------------------------------------------------------------
# Sentinel & None Graceful Degradation
# -----------------------------------------------------------------------------

def test_fuzzy_match_handles_none_and_sentinels_gracefully():
    """Verify that None boundaries and UnsetType variants degrade safely to empty strings."""
    # Both degrade to empty string "" -> "" in "" passes
    compare_strings(UNSET, None, exact_match=False)
    compare_strings(None, UNSET, exact_match=False)

    # If we look for a concrete token inside an UNSET/None value, it must raise AssertionError
    with pytest.raises(AssertionError):
        compare_strings("token", UNSET, exact_match=False)