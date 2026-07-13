"""
Tests for process_params — strict normalization of explicit parameter containers into executable args and kwargs.
"""
import sys
import pytest
from _pytest.outcomes import Failed

from simplibs.exception.testing.tools.Kwargs import Kwargs
from simplibs.exception.testing.asserts.functions._utils.process_params import process_params


# -----------------------------------------------------------------------------
# 1. Explicit Keyword Wrapper (Kwargs)
# -----------------------------------------------------------------------------

def test_naked_kwargs_maps_directly_to_keyword_space():
    """Verify that a standalone Kwargs instance unpacks fully into kwargs and leaves args empty."""
    params = Kwargs(mode="strict", timeout=10)
    args, kwargs = process_params(params)

    assert args == ()
    assert kwargs == {"mode": "strict", "timeout": 10}


# -----------------------------------------------------------------------------
# 2. Strict Tuple Mapping & Unpacking
# -----------------------------------------------------------------------------

def test_pure_tuple_maps_to_positional_arguments():
    """Verify that standard tuples are converted directly to positional args."""
    args, kwargs = process_params((1, "test", True))

    assert args == (1, "test", True)
    assert kwargs == {}


def test_tuple_with_trailing_kwargs_unpacks_correctly():
    """Verify that a tuple with a Kwargs object at the end splits into positional args and named kwargs."""
    params = (100, "prod", Kwargs(verbose=True, retries=3))
    args, kwargs = process_params(params)

    assert args == (100, "prod")
    assert kwargs == {"verbose": True, "retries": 3}


def test_nested_tuple_is_preserved_safely_as_single_positional_argument():
    """Architectural Rule: Nested tuples represent a single positional collection argument.

    This guarantees absolute determinism, completely replacing the deprecated Param wrapper.
    """
    params = (("a.py", "b.py"),)
    args, kwargs = process_params(params)

    assert args == (("a.py", "b.py"),)
    assert kwargs == {}


# -----------------------------------------------------------------------------
# 3. Framework Guard Interception (Negative Testing)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize(
    "invalid_container",
    [
        "flat-string",                      # Primitive scalar
        12345,                              # Numeric scalar
        [42, "fallback"],                   # Mutable list (rejected in favor of strict tuples)
        {"settings_key": "value"},          # Raw dictionary
    ]
)
def test_process_params_triggers_framework_guard_on_invalid_types(invalid_container):
    """Verify that any payload container violating the explicit tuple/Kwargs contract is intercepted."""
    # The framework guard must explicitly halt execution via pytest.fail(), raising a Failed exception
    with pytest.raises(Failed) as exc_info:
        process_params(invalid_container)

    # Validate that the diagnostic educational guide is included in the output message
    assert "[Framework Guard] Invalid parameter container type detected!" in str(exc_info.value)
    assert "💡 Tip: All test parameters must be wrapped in a tuple." in str(exc_info.value)