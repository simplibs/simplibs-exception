import pytest
from simplibs.exception.testing.asserts.fields._utils.compare_strings import compare_strings


def test_compare_exact_match():
    """Verify strict equality mode."""
    compare_strings("abc", "abc", exact_match=True)
    with pytest.raises(AssertionError):
        compare_strings("abc", "abcd", exact_match=True)


def test_compare_startswith():
    """Verify prefix validation mode."""
    compare_strings("abc", "abcdef", startswith=True)
    with pytest.raises(AssertionError):
        compare_strings("xyz", "abcdef", startswith=True)


def test_compare_fuzzy_match():
    """Verify default substring inclusion mode."""
    compare_strings("denied", "Access denied")
    with pytest.raises(AssertionError):
        compare_strings("missing", "Access denied")


def test_compare_with_normalization():
    """Verify that tuples and sentinels are normalized before comparison."""
    # Tuple normalization
    compare_strings(("ip", "127.0.0.1"), ("ip", "127.0.0.1"), exact_match=True)

    # None/Unset normalization (both become "")
    compare_strings(None, None, exact_match=True)