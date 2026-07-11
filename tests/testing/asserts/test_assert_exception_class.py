"""
Tests for assert_exception_class — facade orchestration, deep check branches, and verbosity cascades.
"""
import sys
import pytest

# Force bypassing the __init__.py function re-export to grab the actual file module object
import simplibs.exception.testing.asserts.assert_exception_class as _raw_module
assert_exception_class_mod = sys.modules["simplibs.exception.testing.asserts.assert_exception_class"]

# Now extract the executable target from the verified module layer
from simplibs.exception.testing.asserts.assert_exception_class import assert_exception_class


# -----------------------------------------------------------------------------
# Test Tracking Spies
# -----------------------------------------------------------------------------

class PipelineTracker:
    """Spy container tracking the exact execution footprint and arguments of sub-modules."""
    def __init__(self) -> None:
        self.calls = []

    def track(self, stage_name: str, **kwargs: str) -> None:
        self.calls.append({"stage": stage_name, "kwargs": kwargs})


class DummyClass:
    """Mock target class passing through the pipeline orchestration loop."""
    pass


# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

def test_full_pipeline_orchestration_under_deep_check(monkeypatch):
    """Verify that all four stages are sequentially invoked when deep_check is enabled."""
    tracker = PipelineTracker()
    subtests_dummy = "pytest-subtests-manager"

    # Patch the local references directly inside the target file module scope
    monkeypatch.setattr(
        assert_exception_class_mod, "assert_class_inheritance",
        lambda subtests, exc_class, verbose, intro: tracker.track(
            "inheritance", verbose=verbose, intro=intro
        )
    )
    monkeypatch.setattr(
        assert_exception_class_mod, "assert_class_defaults",
        lambda subtests, exc_class, exact_match, verbose, intro: tracker.track(
            "defaults", verbose=verbose, intro=intro
        ) or "mock-vanilla-instance"
    )
    monkeypatch.setattr(
        assert_exception_class_mod, "assert_class_constructor",
        lambda subtests, exc_class, verbose, intro: tracker.track(
            "constructor", verbose=verbose, intro=intro
        )
    )
    monkeypatch.setattr(
        assert_exception_class_mod, "assert_class_interface",
        lambda subtests, exc_class, verbose, intro: tracker.track(
            "interface", verbose=verbose, intro=intro
        )
    )

    # Trigger the orchestrator facade with deep_check active
    result = assert_exception_class(
        subtests_dummy, DummyClass,
        exact_match=True,
        verbose=True,
        verbose_constructor=False,
        intro="namespace::",
        deep_check=True
    )

    # 1. Verify fluid API returns the vanilla instance captured during the defaults stage
    assert result == "mock-vanilla-instance"

    # 2. Verify all stages were called in strict sequential order
    assert len(tracker.calls) == 4
    assert [c["stage"] for c in tracker.calls] == ["inheritance", "defaults", "constructor", "interface"]

    # 3. Verify that arguments were successfully forwarded down the chain
    for call in tracker.calls:
        assert call["kwargs"]["intro"] == "namespace::"


def test_deep_check_deactivation_skips_extended_structural_audits(monkeypatch):
    """Verify that disabling deep_check caps execution at inheritance and default values stages."""
    tracker = PipelineTracker()

    monkeypatch.setattr(assert_exception_class_mod, "assert_class_inheritance", lambda *a, **kw: tracker.track("inheritance"))
    monkeypatch.setattr(assert_exception_class_mod, "assert_class_defaults", lambda *a, **kw: tracker.track("defaults"))
    monkeypatch.setattr(assert_exception_class_mod, "assert_class_constructor", lambda *a, **kw: tracker.track("constructor"))
    monkeypatch.setattr(assert_exception_class_mod, "assert_class_interface", lambda *a, **kw: tracker.track("interface"))

    # Trigger with deep_check turned OFF
    assert_exception_class(None, DummyClass, deep_check=False)

    # Extended constructor and interface checks must be skipped completely
    assert len(tracker.calls) == 2
    assert [c["stage"] for c in tracker.calls] == ["inheritance", "defaults"]


def test_verbosity_cascading_logic_gates(monkeypatch):
    """Verify the two-tier verbosity hierarchy and constructor master suppression switch."""
    tracker = PipelineTracker()

    monkeypatch.setattr(assert_exception_class_mod, "assert_class_inheritance", lambda *a, **kw: None)
    monkeypatch.setattr(assert_exception_class_mod, "assert_class_defaults", lambda *a, **kw: None)
    monkeypatch.setattr(assert_exception_class_mod, "assert_class_interface", lambda *a, **kw: None)
    monkeypatch.setattr(
        assert_exception_class_mod, "assert_class_constructor",
        lambda subtests, exc_class, verbose, intro: tracker.track("constructor", verbose=verbose)
    )

    # Scenario A: Global verbose is True, local verbose_constructor is True -> Constructor receives True
    assert_exception_class(None, DummyClass, verbose=True, verbose_constructor=True)
    assert tracker.calls[-1]["kwargs"]["verbose"] is True

    # Scenario B: Global verbose is True, local verbose_constructor is False -> Constructor receives False
    assert_exception_class(None, DummyClass, verbose=True, verbose_constructor=False)
    assert tracker.calls[-1]["kwargs"]["verbose"] is False

    # Scenario C: Master Suppression Gate. Global verbose is False, local verbose_constructor is True -> Constructor MUST receive False
    assert_exception_class(None, DummyClass, verbose=False, verbose_constructor=True)
    assert tracker.calls[-1]["kwargs"]["verbose"] is False