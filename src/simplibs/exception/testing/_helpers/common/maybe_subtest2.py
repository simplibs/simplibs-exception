from contextlib import contextmanager
from types import TracebackType
from typing import Any, Iterator


@contextmanager
def maybe_subtest(
    subtests: Any,
    *,
    name: str,
    verbose: bool,
) -> Iterator[Any]:
    """Conditionally create a pytest subtest context.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        name: Human-readable diagnostic label.
        verbose: Whether subtests should be enabled.

    Yields:
        The subtest context result when verbose, otherwise None.
    """
    if verbose:
        with subtests.test(name) as ctx:
            yield ctx
    else:
        yield None