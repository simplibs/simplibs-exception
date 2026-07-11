from typing import Any, Callable
# Outers
from ...tools import maybe_subtest


def assert_function_callable(
    subtests: Any,
    func: Callable[..., Any],
    *,
    verbose: bool = True,
    intro: str = "",
) -> Callable[..., Any]:
    """Assert that the target verification object is natively callable.

    Validates that the supplied routing target can be invoked as a standard function
    boundary before any parametric execution routines are executed.

    Args:
        subtests: The native pytest subtests fixture manager instance.
        func: The target logic block or validation function under test.
        verbose: Enables isolated pytest subtest key routing.
        intro: Optional prefix string added to the generated subtest identity name.

    Returns:
        The verified callable object instance.
    """

    with maybe_subtest(
        subtests,
        name=f"{intro}test_callable",
        verbose=verbose,
    ):
        assert callable(func)

    return func


_DESIGN_NOTES = """
# assert_function_callable (Operational Interface Gate)

## Purpose
Acts as the immediate runtime validation gate for function-driven test pipelines. It ensures that 
any target passed into the testing macros matches Python's execution requirements before internal 
parameter normalizers and invocation engines attempt execution.

## Pipeline Lifecycle Role
This routine serves as a Fail-Fast sentinel within composite runners such as `assert_exception_function`. 
By throwing a strict assertion error early if a non-callable object (e.g., an accidental raw string, 
integer, or incorrectly typed configuration token) is provided, it prevents unhandled internal 
`TypeError: '...' object is not callable` crashes, ensuring diagnostic reports remain clear and precise.
"""