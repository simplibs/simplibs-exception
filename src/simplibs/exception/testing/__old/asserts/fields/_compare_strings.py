from simplibs.sentinels import UnsetType

from ._normalize_value import normalize

def compare_strings(
    test_value: str | tuple[str, ...] | None | UnsetType,
    exc_value: str | tuple[str, ...] | None | UnsetType,
    *,
    exact_match: bool = False,
    startswith: bool = False,
) -> None:
    """Compare evaluation string metrics against target exception outputs.

    Evaluation hierarchy:
    1. Exact Match (if exact_match=True)
    2. Starts With (if startswith=True)
    3. Substring Inclusion (default)
    """

    normalized_test = normalize(test_value)
    normalized_exc = normalize(exc_value)

    # 1. Absolute Equality Mode
    if exact_match:
        assert normalized_test == normalized_exc
        return

    # 2. Prefix Mode
    if startswith:
        assert normalized_exc.startswith(normalized_test)
        return

    # 3. Fuzzy Substring Mode (Default)
    assert normalized_test in normalized_exc