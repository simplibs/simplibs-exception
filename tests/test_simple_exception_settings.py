"""
Tests for SimpleExceptionSettings — validation of instantiation guards, defaults, and factory reset pipelines.
"""
import pytest

from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings
from simplibs.exception._core_logic.internal_exceptions.SimpleExceptionSettingsError import (
    SimpleExceptionSettingsError,
)
from simplibs.exception.modes.PRETTY import PRETTY
from simplibs.exception.modes.SIMPLE import SIMPLE
from simplibs.exception.testing import assert_exception_function


# -----------------------------------------------------------------------------
# 1. Instantiation Guard Audits (Framework-Driven)
# -----------------------------------------------------------------------------

def test_cannot_be_instantiated_raises_with_perfect_telemetry(subtests):
    """Confirms that the registry acts as a static namespace and prevents accidental object instantiation.

    Leverages the centralized framework validation engine to verify the completeness
    of diagnostic logs and recovery actions.
    """
    assert_exception_function(
        subtests,
        # TRICK: Passing the class itself as the target callable engine
        SimpleExceptionSettings,
        invalid_params=(),  # Attempting to call the constructor without arguments
        exception_type=SimpleExceptionSettingsError,
        label="SimpleExceptionSettings",
        problem="This configuration registry class is not intended to be instantiated.",
        how_to_fix=(
            "Access or modify configuration attributes directly on the class: SimpleExceptionSettings.GET_LOCATION",
            "To restore factory defaults programmatically, call: SimpleExceptionSettings.reset()",
        ),
    )


# -----------------------------------------------------------------------------
# 2. Immutable System Boundary Verification
# -----------------------------------------------------------------------------

def test_system_blacklist_contains_expected_default_patterns():
    """Verifies that the core system-protected exclusion patterns are present for stack frame pruning."""
    assert "<" in SimpleExceptionSettings._SYSTEM_BLACKLIST
    assert "simplibs/exception" in SimpleExceptionSettings._SYSTEM_BLACKLIST


# -----------------------------------------------------------------------------
# 3. State Mutation & Factory Reset Pipelines
# -----------------------------------------------------------------------------

def test_reset_restores_get_location_default():
    """Ensures runtime overrides to call-site traversal depth are wiped by factory reset."""
    SimpleExceptionSettings.GET_LOCATION = 5
    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings.GET_LOCATION == 1


def test_reset_restores_value_truncation_length_default():
    """Validates that string clipping boundaries are restored to their production default after reset."""
    SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH = 999
    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings.VALUE_TRUNCATION_LENGTH == 70


def test_reset_restores_message_mode_default():
    """Confirms that the active presentation strategy resets to the PRETTY (default) mode."""
    SimpleExceptionSettings.MESSAGE_MODE = SIMPLE
    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings.MESSAGE_MODE is PRETTY


def test_reset_clears_dynamic_cls_cache():
    """Verifies that internal memoization caches for synthetic exception classes are cleared during reset."""
    # Bypass metaclass validation to inject mock cache entry for testing
    type.__setattr__(SimpleExceptionSettings, "_dynamic_cls_cache", {"fake": "entry"})
    assert SimpleExceptionSettings._dynamic_cls_cache == {"fake": "entry"}

    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings._dynamic_cls_cache == {}


def test_reset_location_blacklist_consistency():
    """Validates that factory reset clears user-defined blacklist additions."""
    SimpleExceptionSettings.LOCATION_BLACKLIST = ("something.py",)
    SimpleExceptionSettings.reset()
    assert SimpleExceptionSettings.LOCATION_BLACKLIST == ()