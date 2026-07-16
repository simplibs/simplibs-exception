# 🌋 `exceptions_bulk_test`

**Automated Subsystem Matrix Testing**

The `bulk_test` package provides the highest-level orchestration layer 
within the `SimpleException` testing framework. 
This automated engine allows developers to write **a single, unified test** 
that comprehensively validates an entire subsystem architecture 
(exception classes, validation functions, and complex scenarios).

## 💡 Table of Contents:
> * [⚙️ Architectural Principles](#-architectural-principles)
> * [🧭 Test Item Formats (Supported Signatures)](#-test-item-formats-supported-signatures)
> * [🔍 Quick Matrix Preview](#-quick-matrix-preview)
> * [🛠️ Configuration & Parameters](#-configuration--parameters)
> * [🧪 Under-the-Hood Routing Mechanics](#-under-the-hood-routing-mechanics)
> * [📖 Real-World Practical Example: Testing Settings Subsystem](#-real-world-practical-example-testing-settings-subsystem)
> * [📊 Terminal Output Visual Representation](#-terminal-output-visual-representation)

---

## ⚙️ Architectural Principles

* **Automated Dynamic Routing:** 
The execution engine inspects signature footprints at runtime 
to dynamically dispatch each item to its corresponding dedicated auditor.
* **Elimination of Duplication:** 
Standardizes validation boundaries by allowing developers to assert 
an entire subsystem’s integrity via a clean, unified array of `ITEMS`.
* **Flexible Execution Modes (Shallow vs. Deep):** 
Supports toggling between rapid smoke validation (optimized for fast-pass CI pipelines)
and exhaustive deep compliance auditing.

---

## 🧭 Test Item Formats (Supported Signatures)

The `exceptions_bulk_test` orchestrator automatically detects and processes three structural formats:

1. **Naked Exception Class** (`SimpleExceptionInternalError`)
A raw class blueprint. Routed to `assert_exception_class` to perform basic inheritance, 
defaults, and interface evaluations.
2. **Inline Functional Sequence** (`tuple(ExceptionClass, Callable, *Parameters)`)
A compact layout representing quick failure boundaries. Routed to `assert_exception_function` 
with deep field assertions disabled.
3. **Complex Test Scenario** (`FuncCase`)
A declarative configuration container. Triggers complete compliance verification 
across all populated dynamic telemetry fields.

[▲ Back to Top](#-exceptions_bulk_test)

---

## 🔍 Quick Matrix Preview

```python
exceptions_bulk_test(
    subtests,
    items=[
        MyException,                                # 1. Class-level structural audit
        (MyException, validate_input, "bad_input"), # 2. Inline functional sequence check
        FuncCase(                                   # 3. Complex declarative scenario
            func=validate_input,
            invalid_params=("bad_input",),
            exception_type=MyException,
            message="Expected diagnostic message",
        )
    ],
    deep_check=False
)
```

[▲ Back to Top](#-exceptions_bulk_test)

---

## 🛠️ Configuration & Parameters

### Mandatory Parameters

* **`subtests`** (`Any`): The native pytest subtests fixture manager instance.
* **`items`** (`list[Any]`): A heterogeneous collection of validation targets.

### Optional Parameters

* **`exact_match`** (`bool`): 
Default: `False`. 
Enforces strict exact string equality checks (using the `==` operator) across string attributes.
* **`startswith`** (`bool`): 
Default: `False`. 
Validates that targeted string attributes begin with the expected substring.
* **`verbose`** (`bool`): 
Default: `True`. 
Isolates each active component audit into its own named pytest subtest frame.
* **`deep_check`** (`bool`): 
Default: `False`. 
If `True`, routes raw exception classes through full constructor propagation and serialization audits.

### Raises:

* **`AssertionError`**: If an item in the collection fails to match any supported format signature.

### Return Value

* **`None`**: This pipeline acts purely as an assertion execution gate and does not return a value.

```python
# Function signature:
def exceptions_bulk_test(
    subtests: Any,
    items: list[Any],
    *,
    exact_match: bool = False,
    startswith: bool = False,
    verbose: bool = True,
    deep_check: bool = False,
) -> None:
```

[▲ Back to Top](#-exceptions_bulk_test)

---

## 🧪 Under-the-Hood Routing Mechanics

When a sequence of targets is passed into `exceptions_bulk_test`, 
the orchestrator iterates through the collection and applies the following routing logic:

```python
for item in items:
    # 1. Process explicit composite testing contexts encapsulated as FuncCase objects
    if isinstance(item, FuncCase):
        item.run_test(
            subtests,
            exact_match=exact_match,
            startswith=startswith,
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )

    # 2. Process raw naked exception classes (Structural blueprint audits)
    elif is_exception_class(item):
        exc_class = item
        assert_exception_class(
            subtests,
            exc_class,
            exact_match=exact_match,
            startswith=startswith,
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )

    # 3. Process raw parametric inline sequences wrapped in basic tuples
    elif is_exception_function(item):
        # Unpacking tuple signature footprint: (ExceptionClass, Callable, *Parameters)
        exc_class, func, raw_params = item[0], item[1], item[2:]
        assert_exception_function(
            subtests,
            func,
            invalid_params=raw_params,
            exception_type=exc_class,
            exact_match=exact_match,
            startswith=startswith,
            verbose=verbose,
            intro=intro,
            deep_check=False,
        )
        
    # 4. Fallback gate throwing strict alerts on invalid format tokens
    else:
        with maybe_subtest(subtests, name="unknown_item", verbose=verbose):
            raise AssertionError(f"Unsupported item signature footprint: {item!r}")           
```

[▲ Back to Top](#-exceptions_bulk_test)

---

## 📖 Real-World Practical Example: Testing Settings Subsystem

The following practical scenario demonstrates how a single test matrix 
comprehensively evaluates three exception classes, one complex `FuncCase` scenario 
containing detailed field assertions, and seven distinct validation functions.

### Component Setup & Matrix Declaration:

```python
import pytest
from simplibs.exception._core_logic.internal_exceptions import (
    SimpleExceptionInternalError, SimpleExceptionModeError, SimpleExceptionSettingsError
)
from simplibs.exception._core_logic.settings_meta.validations import (
    raise_unknown_settings_attribute_error, raise_system_blacklist_mutation_error,
    validate_dynamic_cls_cache, validate_get_location, validate_location_blacklist,
    validate_message_mode, validate_value_truncation_length
)

# Mock class representing target inputs
class DummyClass:
    _VALIDATORS = {"GET_LOCATION": validate_get_location}

# 1. Complex configuration scenario for the cache validator
VALIDATE_DYNAMIC_CLS_CACHE_CASE = FuncCase(
    func=validate_dynamic_cls_cache,
    valid_params={},
    invalid_params="abc",
    exception_type=SimpleExceptionSettingsError,
    error_name="SETTINGS ERROR",
    label="_dynamic_cls_cache",
    expected="an empty dict {} — for configuration and state reset routines only",
    value="abc",
    problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
    how_to_fix=(
        "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
        "To clear this cache manually during hot-reloads or tests, assign an empty dict: SimpleExceptionSettings._dynamic_cls_cache = {}",
    )
)

# 2. Assembling the complete subsystem test matrix
ITEMS = [
    # A) Exception Classes (Structural contract compliance)
    SimpleExceptionInternalError,
    SimpleExceptionModeError,
    SimpleExceptionSettingsError,

    # B) Complex Scenario (Deep telemetry properties check)
    VALIDATE_DYNAMIC_CLS_CACHE_CASE,

    # C) Inline Functional Intercepts (Positional parameters)
    (SimpleExceptionSettingsError, raise_unknown_settings_attribute_error, DummyClass, "name"),
    (SimpleExceptionSettingsError, raise_system_blacklist_mutation_error, "value"),
    (SimpleExceptionSettingsError, validate_dynamic_cls_cache, "invalid_input"),
    (SimpleExceptionSettingsError, validate_get_location, "invalid_input"),
    (SimpleExceptionSettingsError, validate_location_blacklist, "invalid_input"),
    (SimpleExceptionSettingsError, validate_location_blacklist, (1,)),
    (SimpleExceptionSettingsError, validate_message_mode, "invalid_input"),
    (SimpleExceptionSettingsError, validate_value_truncation_length, "invalid_input"),
    (SimpleExceptionSettingsError, validate_value_truncation_length, -1),
]

def test_settings_subsystem_bulk(subtests):
    """A single master test case evaluating the entire settings subsystem layout."""
    exceptions_bulk_test(
        subtests, 
        ITEMS, 
        verbose=True, 
        deep_check=False  # Configured to False for high-speed smoke checks
    )
```

[▲ Back to Top](#-exceptions_bulk_test)

---

## 📊 Terminal Output Visual Representation

When running the subsystem matrix with `verbose=True`, pytest utilizes subtests 
to generate an organized, hierarchical output tree. Every component receives 
its own namespace prefix dynamically built from class or callable names:

```text
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_SimpleExceptionInternalError::test_class_inheritance::test_base_exception_inheritance]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_SimpleExceptionInternalError::test_class_defaults::test_error_name]
...
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_callable]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_raises_exception]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_label]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_problem]
...
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_raise_unknown_settings_attribute_error::test_callable]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_raise_unknown_settings_attribute_error::test_raises_exception]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_value_truncation_length::test_raises_exception]
test_bulk.py::test_settings_subsystem_bulk PASSED
```

If you switch the configuration to `verbose=False`, this extensive evaluation sweeps down 
into a single clean line in your execution summary:

```text
test_bulk.py::test_settings_subsystem_bulk PASSED
```

[▲ Back to Top](#-exceptions_bulk_test)

---

[⬅️ Back to README_TESTING](../README_TESTING.md)  
[⬅️ Back to README](../../../README.md)