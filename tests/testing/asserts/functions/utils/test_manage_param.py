"""
Tests for manage_param — normalization of raw dynamic parameters into executable args and kwargs.
"""
from simplibs.exception.testing.tools.Kwargs import Kwargs
from simplibs.exception.testing.tools.Param import Param
from simplibs.exception.testing.asserts.functions._utils.manage_param import manage_param


# -----------------------------------------------------------------------------
# 1. Explicit Keyword Wrapper (Kwargs)
# -----------------------------------------------------------------------------

def test_naked_kwargs_maps_directly_to_keyword_space():
    """Verify that a standalone Kwargs instance unpacks fully into kwargs and leaves args empty."""
    param = Kwargs(mode="strict", timeout=10)
    args, kwargs = manage_param(param)

    assert args == ()
    assert kwargs == {"mode": "strict", "timeout": 10}


# -----------------------------------------------------------------------------
# 2. Sequence Mapping (tuple / list)
# -----------------------------------------------------------------------------

def test_pure_sequence_maps_to_positional_arguments():
    """Verify that standard sequences are converted to a pure positional args tuple."""
    # Tuple pass
    args, kwargs = manage_param((1, "test", True))
    assert args == (1, "test", True)
    assert kwargs == {}

    # List pass
    args, kwargs = manage_param([42, "fallback"])
    assert args == (42, "fallback")
    assert kwargs == {}


def test_sequence_with_trailing_kwargs_unpacks_correctly():
    """Verify that a sequence with Kwargs at the end splits into positional args and named kwargs."""
    param = (100, "prod", Kwargs(verbose=True, retries=3))
    args, kwargs = manage_param(param)

    assert args == (100, "prod")
    assert kwargs == {"verbose": True, "retries": 3}


def test_sequence_deep_scan_unwraps_nested_param_guards():
    """Verify that sequence routing automatically unwarps any embedded Param guards found inside slots."""
    param = ("mock-cls", Param(("a.py", "b.py")), Kwargs(strict=True))
    args, kwargs = manage_param(param)

    # The inner tuple must be cleanly unwrapped as a single item inside the args tuple
    assert args == ("mock-cls", ("a.py", "b.py"))
    assert kwargs == {"strict": True}


# -----------------------------------------------------------------------------
# 3. Standalone Param Isolation Guard
# -----------------------------------------------------------------------------

def test_standalone_param_unwraps_collections_safely():
    """Verify that wrapping a collection in Param protects it from flattening, delivering it as a single unit."""
    # Standalone full tuple
    args, kwargs = manage_param(Param(("a.py", "b.py")))
    assert args == (("a.py", "b.py"),)
    assert kwargs == {}

    # Standalone empty tuple
    args, kwargs = manage_param(Param(()))
    assert args == ((),)
    assert kwargs == {}


# -----------------------------------------------------------------------------
# 4. Scalar & Raw Dictionary Fallback
# -----------------------------------------------------------------------------

def test_scalars_and_primitives_wrap_into_single_item_args():
    """Verify that primitive scalars are wrapped into a single-item positional tuple."""
    args, kwargs = manage_param("flat-string")
    assert args == ("flat-string",)
    assert kwargs == {}

    args, kwargs = manage_param(12345)
    assert args == (12345,)
    assert kwargs == {}


def test_raw_dictionaries_treated_strictly_as_positional_arguments():
    """Architectural Rule: Raw dicts must NEVER automatically expand into kwargs."""
    raw_dict = {"settings_key": "value"}
    args, kwargs = manage_param(raw_dict)

    assert args == (raw_dict,)
    assert kwargs == {}