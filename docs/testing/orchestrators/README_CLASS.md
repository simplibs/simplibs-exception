# 📦 `assert_exception_class`

**Comprehensive Exception Class Audit**

`assert_exception_class` is the primary orchestrator implementing the **Facade** pattern 
within the `SimpleException` testing infrastructure. 
It unifies four granular, isolated compliance audits into a single, 
predictable, sequential verification pipeline.

## 💡 Table of Contents:
> * [⚙️ Architectural Principles](#-architectural-principles)
> * [🧭 Pipeline Execution Flow](#-pipeline-execution-flow)
> * [🔍 Quick Usage Examples](#-quick-usage-examples)
> * [🛠️ Configuration & Parameters](#-configuration--parameters)
> * [🔄 Audit Pipeline (4 Phases)](#-audit-pipeline-4-phases)
>   * [Phase 1: Inheritance Hierarchy (Fail-Fast Gate)](#phase-1-inheritance-hierarchy-fail-fast-gate)
>   * [Phase 2: Class Defaults Reflection](#phase-2-class-defaults-reflection)
>   * [Phase 3: Constructor Propagation](#phase-3-constructor-propagation-triggered-when-deep_checktrue)
>   * [Phase 4: Public API & Serializers](#phase-4-public-api--serializers-triggered-when-deep_checktrue)
> * [📖 Real-World Examples](#-real-world-examples)
> * [📊 Terminal Output Comparison](#-terminal-output-comparison)

---

## ⚙️ Architectural Principles

* **Facade Pattern:** 
Orchestrates multiple low-level structural evaluations through a single master gateway.
* **Fail-Fast Gate:** 
Halts pipeline execution immediately if basic inheritance contracts are broken, 
protecting subsequent dynamic reflection scanners from raising unpredictable, unreadable crashes.
* **Fluid API:** 
Returns the raw, validated exception instance initialized during the class defaults phase, 
allowing developers to chain custom assertions immediately.
* **Verbosity Hierarchy:** 
Integrates a dual-gate verbosity routing. The global `verbose` parameter 
controls standard pytest subtest generation, while `verbose_constructor` 
acts as a fine-tuning flag for deep parameterization audits.


---

## 🧭 Pipeline Execution Flow

The orchestrator executes its compliance checks in a strict, dependency-ordered sequence:

1. **Inheritance Contract** (`assert_class_inheritance`)
Verifies that the exception class natively derives from `BaseException` 
and `SimpleExceptionData` (plus optional custom polymorphic base blueprints).
2. **Class Defaults Reflection** (`assert_class_defaults`)
Verifies that parameterless instantiation correctly inherits fallback class-level properties. 
Returns this vanilla exception instance.
3. **Constructor Propagation** (`assert_class_constructor`)
*Executed only when `deep_check=True`.* Audits the state initialization boundaries 
of the exception's `__init__` layer.
4. **Public API Contract** (`assert_class_interface`)
*Executed only when `deep_check=True`.* Audits the type compliance of standard 
Python dunder methods and built-in serializátor methods (`to_dict`, `to_json`, etc.).

[▲ Back to Top](#-assert_exception_class)

---

## 🔍 Quick Usage Examples

```python
# 1. Standard comprehensive class audit
assert_exception_class(subtests, MyError)

# 2. Enforcing strict string equality across defaults (Exact match)
assert_exception_class(subtests, MyError, exact_match=True)

# 3. Validating defaults using prefix matching
assert_exception_class(subtests, MyError, startswith=True)

# 4. Silent mode execution without allocating pytest subtest frames
assert_exception_class(subtests, MyError, verbose=False)

# 5. Fast-pass execution (bypassing deep constructor and serialization audits)
assert_exception_class(subtests, MyError, deep_check=False)
```

[▲ Back to Top](#-assert_exception_class)

---

## 🛠️ Configuration & Parameters

Customize the behavior of the orchestrator using the configuration parameters detailed below.

### Mandatory Parameters

* **`subtests`** (`Any`): The native pytest subtests fixture manager instance.
* **`exc_class`** (`type[Any]`): The target exception class to validate.

### Optional Parameters

* **`expected_parents`** (`type[Any] | tuple[type[Any], ...]`): 
Default: `UNSET`. 
A class type or tuple of class types that the target exception must natively inherit from (verifies polymorphic subsystem handling).
* **`exact_match`** (`bool`): 
Default: `False`. 
Enforces strict exact equality comparison on string attributes.
* **`startswith`** (`bool`): 
Default: `False`. 
Validates that targeted string attributes begin with the expected substring.
* **`verbose`** (`bool`): 
Default: `True`. 
The master gate controlling global subtest frame allocation.
* **`verbose_constructor`** (`bool`): 
Default: `False`. 
If `True`, expands individual field propagation checks inside the constructor subtest block.
* **`intro`** (`str`): 
Default: `""`. 
An optional namespace prefix prepended to generated subtest labels.
* **`deep_check`** (`bool`): 
Default: `True`. 
If `True`, executes advanced constructor propagation and public serialization API checks.

### Return Value

* Returns the instantiated exception object captured during the defaults verification run.

```python
# Function signature:
def assert_exception_class(
    subtests: Any,
    exc_class: type[Any],
    *,
    expected_parents: type[Any] | tuple[type[Any], ...] | UnsetType = UNSET,
    exact_match: bool = False,
    startswith: bool = False,
    verbose: bool = True,
    verbose_constructor: bool = False,
    intro: str = "",
    deep_check: bool = True,
) -> BaseException:
```

[▲ Back to Top](#-assert_exception_class)

---

## 🔄 Audit Pipeline (4 Phases)

### Phase 1: Inheritance Hierarchy (Fail-Fast Gate)

This step ensures that the exception class aligns with Python's runtime requirements 
and the framework's internal layout. If this contract is broken, execution halts immediately.

```python
# Internal invocation:
assert_class_inheritance(
    subtests,
    exc_class,
    expected_parents=expected_parents,
    verbose=verbose,
    intro=intro
)

# Executed under the hood:
assert issubclass(exc_class, BaseException)
assert issubclass(exc_class, SimpleExceptionData)
assert issubclass(exc_class, expected_parents)  # Evaluated only if custom parents are supplied
```

### Phase 2: Class Defaults Reflection

The engine initializes a parameterless instance of the exception 
and verifies that its initial states cleanly mirror the static metadata 
declared directly on the class body level.

```python
# Internal invocation:
exc = assert_class_defaults(
    subtests,
    exc_class,
    exact_match=exact_match,
    startswith=startswith,
    verbose=verbose,
    intro=intro
)

# Executed under the hood (attribute extraction and comparison):
class_dict = exc_class.__dict__
return assert_exception_fields(
    subtests,
    exc,
    error_name=class_dict.get("error_name", UNSET),
    label=class_dict.get("label", UNSET),
    message=class_dict.get("message", UNSET),
    expected=class_dict.get("expected", UNSET),
    value=class_dict.get("value", UNSET),
    problem=class_dict.get("problem", UNSET),
    context=class_dict.get("context", UNSET),
    how_to_fix=class_dict.get("how_to_fix", UNSET),
    exception=class_dict.get("exception", UNSET),
    get_location=class_dict.get("get_location", UNSET),
    skip_locations=class_dict.get("skip_locations", UNSET),
    oneline=class_dict.get("oneline", UNSET),
    exact_match=exact_match,
    startswith=startswith,
    verbose=verbose,
    intro=intro + subintro,
)
```

### Phase 3: Constructor Propagation (Triggered when `deep_check=True`)

The engine generates a dense reference telemetry matrix and passes 
it directly into the class constructor. It then audits the active instance 
to confirm that all parameters propagated successfully 
and that core identities are exposed in `str(exc)`.

```python
# Internal invocation:
if deep_check:
    assert_class_constructor(
        subtests,
        exc_class,
        verbose=verbose and verbose_constructor,
        intro=intro
    )

# Executed under the hood:
_message = "<message>"
_value = "<value>"
_label = "<label>"
_expected = "<expected>"
_problem = "<problem>"
_context = "<context>"
_how_to_fix = "<how_to_fix>"
_error_name = "<ERROR_NAME>"
_exception = ValueError("test exception")
_get_location = False
_skip_locations = ("<skip_locations>",)
_oneline = True

# Instantiation of the test object with the full telemetry dataset
dummy_exc = exc_class(
    message=_message,
    value=_value,
    label=_label,
    expected=_expected,
    problem=_problem,
    context=_context,
    how_to_fix=_how_to_fix,
    error_name=_error_name,
    exception=_exception,
    get_location=_get_location,
    skip_locations=_skip_locations,
    oneline=_oneline,
)

# 1. Auditing that the instance layout perfectly mirrors the reference data
assert_exception_fields(
    subtests, dummy_exc,
    message=_message, value=_value, label=_label, expected=_expected,
    problem=_problem, context=_context, how_to_fix=_how_to_fix,
    error_name=_error_name, exception=_exception, get_location=_get_location,
    skip_locations=_skip_locations, oneline=_oneline,
    exact_match=True, verbose=verbose, intro=intro + subintro,
)

# 2. Verifying that core diagnostic identities seep into str()
exc_str = str(dummy_exc)
assert _error_name in exc_str
assert _message in exc_str
```

### Phase 4: Public API & Serializers (Triggered when `deep_check=True`)

The final validation phase guarantees public-facing data integrity. 
It ensures that standard dunder methods yield appropriate types 
and that all built-in serialization channels execute cleanly.

```python
# Internal invocation:
if deep_check:
    assert_class_interface(
        subtests,
        exc_class,
        verbose=verbose,
        intro=intro
    )

# Executed under the hood:
assert isinstance(str(exc), str)
assert isinstance(repr(exc), str)
assert isinstance(exc.to_dict(), dict)
assert isinstance(exc.to_debug_dict(), dict)
assert isinstance(exc.to_json(), str)
```

[▲ Back to Top](#-assert_exception_class)

---

## 📖 Real-World Examples

The following example demonstrates how to audit an internal framework exception. 
This scenario showcases that the assertion suite operates flawlessly even 
on lightweight exception instances constructed on a mix of `SimpleExceptionData` and `Exception`.

### Target Exception Class Under Test

```python
@dataclass
class SimpleExceptionInternalError(SimpleExceptionData, Exception):
    """Internal library exception — bypasses validation, direct output."""

    # Override standard error identifier
    error_name: str = "INTERNAL ERROR"

    def __post_init__(self):
        from ...modes import PRETTY
        rendered_message = PRETTY.render(self, validate=False)
        Exception.__init__(self, rendered_message)
```

### Executing the Test Suites

This test suite demonstrates how `assert_exception_class` takes care 
of standard structure audits, leaving developers free to focus on writing 
specialized functional checks (such as verifying raw formatting modes) downstream.

```python
import pytest

def test_internal_error_basic_contract(subtests):
    """Run the universal verification pipeline for inheritance, defaults, constructor, and API."""
    assert_exception_class(
        subtests,
        SimpleExceptionInternalError,
        verbose=False
    )

def test_str_contains_rendered_pretty_message():
    """Custom Test: Verifying that PRETTY layouts successfully render telemetry."""
    err = SimpleExceptionInternalError(label="my-label", problem="something broke")
    text = str(err)
    assert "INTERNAL ERROR" in text
    assert "my-label" in text
    assert "something broke" in text

def test_skips_validation_and_never_crashes_on_bad_types():
    """Custom Test: Verifying that the internal error ignores invalid parameter types without crashing."""
    err = SimpleExceptionInternalError(label=12345)  # type: ignore
    assert "12345" in str(err)
```

[▲ Back to Top](#-assert_exception_class)

---

## 📊 Terminal Output Comparison

The `verbose` configuration completely transforms how pytest visualizes compliance steps 
in your terminal, letting you swap between granular tracing and high-level summaries.

### Active Verbose Mode (`verbose=True`)

Ideal during development and debugging of new exception definitions — pinpoints 
the exact assertion step that failed.

```text
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_inheritance::test_base_exception_inheritance]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_inheritance::test_simple_exception_data_inheritance]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_defaults::test_error_name]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_str]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_repr]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_to_dict]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_to_debug_dict]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_to_json]
tests/test_internal_error.py::test_internal_error_basic_contract PASSED
tests/test_internal_error.py::test_str_contains_rendered_pretty_message PASSED
tests/test_internal_error.py::test_skips_validation_and_never_crashes_on_bad_types PASSED
```

### Silent Mode (`verbose=False`)

Ideal for standard continuous integration passes — keeps execution lines tidy and focused.

```text
tests/test_internal_error.py::test_internal_error_basic_contract PASSED
tests/test_internal_error.py::test_str_contains_rendered_pretty_message PASSED
tests/test_internal_error.py::test_skips_validation_and_never_crashes_on_bad_types PASSED
```

[▲ Back to Top](#-assert_exception_class)

---

[⬅️ Back to README_TESTING](../README_TESTING.md)  
[⬅️ Back to README](../../../README.md)