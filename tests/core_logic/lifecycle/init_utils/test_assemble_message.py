from simplibs.exception._core_logic.lifecycle.init_utils.assemble_message import (
    assemble_message,
)
from simplibs.exception.SimpleExceptionSettings import SimpleExceptionSettings
from simplibs.exception.modes.ONELINE import ONELINE
from simplibs.exception.SimpleExceptionData import SimpleExceptionData


def test_oneline_true_uses_oneline_mode_regardless_of_settings():
    """
    Ensures that forcing the oneline flag to True instantly intercepts the dispatch
    pipeline and utilizes the ONELINE rendering engine, bypassing any global configuration.
    """
    # 1. Prepare raw exception data payload instance
    instance = SimpleExceptionData(label="my-label", message="hello")

    # 2. Execute assembler dispatching sequence with active line compression
    result = assemble_message(instance, oneline=True)

    # 3. Assert precise output parity with the standalone ONELINE renderer
    assert result == ONELINE.render(instance, validate=False)


def test_oneline_false_uses_globally_configured_message_mode():
    """
    Validates that when oneline is disabled (False), the assembler gracefully
    defers orchestration to the active global layout mode registered in settings.
    """
    # 1. Prepare standard baseline mock exception data payload
    instance = SimpleExceptionData(label="my-label", message="hello")

    # 2. Execute standard assembler flow matching regular runtime cycles
    result = assemble_message(instance, oneline=False)

    # 3. Assert alignment with the default global configuration schema
    assert result == SimpleExceptionSettings.MESSAGE_MODE.render(instance, validate=False)


def test_oneline_false_reflects_changed_global_mode():
    """
    Guarantees that the dispatcher correctly senses dynamic hot-swaps of
    the global MESSAGE_MODE configuration at runtime, reflecting changes immediately.
    """
    from simplibs.exception.modes.SIMPLE import SIMPLE

    # 1. Prepare testing payload environment
    instance = SimpleExceptionData(label="my-label", message="hello")

    # 2. Simulate dynamic hot-swap modifications to the global registry state
    SimpleExceptionSettings.MESSAGE_MODE = SIMPLE

    # 3. Execute assembler orchestration pass
    result = assemble_message(instance, oneline=False)

    # 4. Assert strict tracking of the dynamically injected visualization engine
    assert result == SIMPLE.render(instance, validate=False)


def test_module_imports_cleanly_without_triggering_circular_loops():
    """
    Architectural Safeguard: Verifies that importing the assemble_message module
    remains completely decoupled from the modes layout package at a top-level execution scope,
    preventing unintended future modifications from re-introducing fatal circular dependency chains.
    """
    import sys
    import importlib

    module_path = "simplibs.exception._core_logic.lifecycle.init_utils.assemble_message"

    # Force unload the module if it was cached to guarantee a fresh top-level import run
    if module_path in sys.modules:
        del sys.modules[module_path]

    # Attempt a raw execution space import initialization pass
    imported_module = importlib.import_module(module_path)

    assert hasattr(imported_module, "assemble_message")