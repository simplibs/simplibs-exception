# 📦 `assert_exception_function`

**Comprehensive Functional Logic Audit**

`assert_exception_function` is the primary orchestrator implementing 
the **Facade** pattern within the `SimpleException` functional testing infrastructure. 
It unifies individual behavioral checks across both valid and invalid inputs into a single, 
predictable, sequential verification pipeline.

## 💡 Table of Contents:
> * [⚙️ Architectural Principles](#-architectural-principles)
> * [🧭 Pipeline Execution Flow](#-pipeline-execution-flow)
> * [🔍 Quick Usage Examples](#-quick-usage-examples)
> * [🛠️ Configuration & Parameters](#-configuration--parameters)
> * [🔄 Audit Pipeline (4 Phases)](#-audit-pipeline-4-phases)
>   * [Phase 1: Callable Isolation Gate](#phase-1-callable-isolation-gate)
>   * [Phase 2: Happy Path Clearance](#phase-2-happy-path-clearance)
>   * [Phase 3: Negative Boundary Intercept & Exception Class Audit](#phase-3-negative-boundary-intercept--exception-class-audit)
>   * [Phase 4: Deep Telemetry Field Inspection](#phase-4-deep-telemetry-field-inspection-triggered-when-deep_checktrue)
> * [📖 Real-World Cookbooks](#-real-world-cookbooks)
>   * [Case 1: Auditing an Isolated Negative Scenario](#case-1-auditing-an-isolated-negative-scenario)
>   * [Case 2: Parameterized Test with Happy Path Verification](#case-2-parameterized-test-with-happy-path-verification-valid_params)
>   * [Case 3: Decoupled Positive Path Sweeps and Target Failures](#case-3-decoupled-positive-path-sweeps-and-target-failures)

---

## ⚙️ Architectural Principles

* **Facade Pattern:** 
Unifies callable validation, happy-path safety passes, defensive exception interception, 
and granular field-level property checking into a single testing entry point.
* **Fail-Fast Gate:** 
If the target callable under audit is not an executable object, the pipeline halts immediately, 
protecting subsequent execution steps from raising unreadable Python crashes.
* **Fluid API:** 
Returns the raw, validated exception instance captured during the negative boundary interception, 
allowing developers to chain custom assertions immediately.
* **Opt-in Comparison Modalities:** 
* The engine defaults to substring inclusion (`in` operator) for dynamic error text. 
Stricter assertion paths can be configured on-demand via `exact_match` or `startswith`.

---

## 🧭 Pipeline Execution Flow

The orchestrator executes its compliance checks in a strict, dependency-ordered sequence:

1. **Callable Gate** (`assert_function_callable`)  
Verifies that the target object under audit is actually an executable callable.
2. **Valid Input Sanity Check** (`assert_function_valid_input`)  
*Executed only when `valid_params` is supplied.* Verifies that passing clean, 
nominal inputs allows the function to complete successfully without throwing unexpected exceptions.
3. **Negative Boundary Check** (`assert_function_raises`)  
Executes the target callable with malformed parameters (`invalid_params`) within 
a secure `pytest.raises` block, capturing the raised exception and verifying its class type.
4. **Deep Telemetry Inspection** (`assert_exception_fields`)  
*Executed only when `deep_check=True`.* Runs a highly granular 
compliance sweep against all populated diagnostic attributes inside the captured exception.

[▲ Back to Top](#-assert_exception_function)

---

## 🔍 Quick Usage Examples

```python
# 1. Comprehensive audit (Happy Path validation, exception capture, and field inspection)
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_params=("bad-value",),
    valid_params=("good-value",),
    label="MY_LABEL",
    message="Something went wrong",
)

# 2. High-speed smoke check (verifies only the raised exception type boundary)
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_params=("bad-value",),
    deep_check=False,
)

# 3. Enforcing strict string equality across text fields (Exact match)
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_params=("bad-value",),
    message="Exact Error Message",
    exact_match=True,
)

# 4. Silent mode execution without allocating individual pytest subtest frames
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_params=("bad-value",),
    verbose=False,
)
```

[▲ Back to Top](#-assert_exception_function)

---

## 🛠️ Configuration & Parameters

### Mandatory Parameters

* **`subtests`** (`Any`): 
The native pytest subtests fixture manager instance.
* **`func`** (`Callable[..., Any]`): 
The target validation or logic function under test.
* **`exception_type`** (`type[BaseException]`): 
The expected type blueprint of the raised exception.
* **`invalid_params`** (`tuple | Kwargs`): 
Malformed inputs engineered to trigger the target exception.

### Optional Parameters

* **`valid_params`** (`tuple | Kwargs`): 
Default: `UNSET`. 
Clean nominal parameters expected to pass without raising errors (validates positive functional paths).
* **Telemetry Fields** 
(`error_name`, `label`, `message`, `expected`, `value`, `problem`, `context`, 
`how_to_fix`, `exception`, `get_location`, `skip_locations`, `oneline`): 
Default: `UNSET`. 
Expected property values populated inside the caught exception instance.

### Setting Parameters (Behavioral Toggles)

* **`exact_match`** (`bool`): 
Default: `False`. 
Enforces strict exact string equality checks (using the `==` operator) across string attributes.
* **`startswith`** (`bool`): 
Default: `False`. 
Validates that targeted string attributes begin with the expected substring.
* **`verbose`** (`bool`): 
Default: `True`. 
Isolates each individual telemetry property check into its own pytest subtest frame.
* **`intro`** (`str`): 
Default: `""`. 
An optional namespace prefix prepended to generated subtest labels.
* **`deep_check`** (`bool`): 
Default: `True`. 
If `False`, limits validation to the exception class type and skips the exhaustive telemetry fields check.

### Return Value

* Returns the caught, instantiated exception object to support downstream custom assertions.

```python
# Function signature:
def assert_exception_function(
    # Required parameters:
    subtests: Any,
    func: Callable[..., Any],
    *,
    exception_type: type[BaseException],
    invalid_params: tuple[Any, ...] | Kwargs,
    # Optional parameters:
    valid_params: tuple[Any, ...] | Kwargs | UnsetType = UNSET,
    error_name: str | UnsetType = UNSET,
    label: str | None | UnsetType = UNSET,
    message: str | None | UnsetType = UNSET,
    expected: str | None | UnsetType = UNSET,
    value: Any = UNSET,
    problem: str | tuple[str, ...] | None | UnsetType = UNSET,
    context: str | tuple[str, ...] | None | UnsetType = UNSET,
    how_to_fix: str | tuple[str, ...] | None | UnsetType = UNSET,
    exception: Exception | type[Exception] | None | UnsetType = UNSET,
    get_location: bool | int | UnsetType = UNSET,
    skip_locations: tuple[str, ...] | UnsetType = UNSET,
    oneline: bool | UnsetType = UNSET,
    # Setting parameters:
    exact_match: bool = False,
    startswith: bool = False,
    verbose: bool = True,
    intro: str = "",
    deep_check: bool = True,
) -> BaseException:
```

[▲ Back to Top](#-assert_exception_function)

---

## 🧭 Audit Pipeline (4 Phases)

### Phase 1: Callable Isolation Gate

The testing engine first validates that the supplied object conforms 
to standard Python runtime expectations and can be safely invoked.

```python
# Internal invocation:
assert_function_callable(
    subtests,
    func,
    verbose=verbose, 
    intro=intro
)

# Executed under the hood:
assert callable(func)
```

### Phase 2: Happy Path Clearance

If you supply parameters to `valid_params`, the orchestrator unpacks them 
and runs a trial execution. This ensures that stable inputs pass cleanly 
and that the code path is not permanently broken.

```python
# Internal invocation:
if valid_params is not UNSET:
    assert_function_valid_input(
        subtests,
        func,
        valid_params=valid_params,
        verbose=verbose,
        intro=intro
    )
    
# Executed under the hood:
args, kwargs = process_params(valid_params)
func(*args, **kwargs)  # Must execute without raising any exception subclass
```

### Phase 3: Negative Boundary Intercept & Exception Class Audit

The engine executes the target callable with the malformed parameters 
from `invalid_params` inside a secure `pytest.raises` zone. 
If the function fails to raise an exception, or raises an unexpected error type 
(like a raw `TypeError` from signature mismatch), the **Framework Guard** 
intercepts execution and fails the test with explicit diagnostics.

```python
# Internal invocation:
exc = assert_function_raises(
    subtests,
    func,
    invalid_params=invalid_params,
    exception_type=exception_type,
    verbose=verbose,
    intro=intro
)

# Executed under the hood:
args, kwargs = process_params(invalid_params)

with pytest.raises(BaseException) as exc_info:
    func(*args, **kwargs)

exc = exc_info.value  # Extracted live exception instance

# Exception type compliance check (Framework Guard)
if not isinstance(exc, exception_type):
    pytest.fail("[Framework Guard] Target callable raised an unexpected exception class type!")

assert isinstance(exc, exception_type)
```

### Phase 4: Deep Telemetry Field Inspection (Triggered when `deep_check=True`)

In the final phase, the engine performs a deep field audit against the attributes stored 
within the captured exception. By default, it uses flexible substring searching (`in`), 
which prevents tests from failing over minor formatting or whitespace updates.

```python
# Internal invocation:
if deep_check:
    assert_exception_fields(
        subtests,
        exc,
        error_name=error_name,
        label=label,
        message=message,
        expected=expected,
        value=value,
        problem=problem,
        context=context,
        how_to_fix=how_to_fix,
        exception=exception,
        get_location=get_location,
        skip_locations=skip_locations,
        oneline=oneline,
        exact_match=exact_match,
        startswith=startswith,
        verbose=verbose,
        intro=intro
    )

# Executed under the hood:
if error_name is not UNSET:
    assert error_name in exc.error_name

if label is not UNSET:
    assert label in exc.label

if message is not UNSET:
    assert message in exc.message

if expected is not UNSET:
    assert expected in exc.expected

if value is not UNSET:
    assert value == exc.value

if problem is not UNSET:
    assert problem in exc.problem

if context is not UNSET:
    assert context in exc.context

if how_to_fix is not UNSET:
    assert how_to_fix in exc.how_to_fix

if exception is not UNSET:
    assert exception == exc.exception

if get_location is not UNSET:
    assert get_location == exc.get_location

if skip_locations is not UNSET:
    assert skip_locations == exc.skip_locations

if oneline is not UNSET:
    assert oneline == exc.oneline
```

[▲ Back to Top](#-assert_exception_function)

---

## 📖 Real-World Cookbooks

### Case 1: Auditing an Isolated Negative Scenario

Consider a function designed to protect read-only system configurations. 
It throws a structured exception if anyone attempts to overwrite the protected system blacklist.

```python
def raise_system_blacklist_mutation_error(value: Any) -> NoReturn:
    """Raises a structured error upon attempts to modify read-only system metadata."""
    raise SimpleExceptionSettingsError(
        value=value,
        label="SimpleExceptionSettings",
        problem="The protected '_SYSTEM_BLACKLIST' attribute is strict read-only metadata.",
        how_to_fix=(
            "Do not attempt to alter the core framework system-level blacklist.",
            "To skip your custom repository paths or wrapper files, append them to: SimpleExceptionSettings.LOCATION_BLACKLIST",
        ),
    )
```

#### Test Suite Implementation

We can verify this entire contract using a single clean, declarative testing block:

```python
def test_raise_system_blacklist_mutation_error(subtests):
    """Verify that the utility terminates execution with a precisely populated exception."""
    assert_exception_function(
        subtests,
        raise_system_blacklist_mutation_error,
        invalid_params=("bad-value",),
        exception_type=SimpleExceptionSettingsError,
        value="bad-value",
        label="SimpleExceptionSettings",
        problem="The protected '_SYSTEM_BLACKLIST' attribute is strict read-only metadata.",
        how_to_fix=(
            "Do not attempt to alter the core framework system-level blacklist.",
            "To skip your custom repository paths or wrapper files, append them to: SimpleExceptionSettings.LOCATION_BLACKLIST",
        ),
    )
```

#### Console Reporting Output for Case 1

* **Active Verbose Mode (`verbose=True` - Granular Property Tracing):**

```text
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_callable]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_raises_exception]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_exception_type]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_label]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_value]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_problem]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_how_to_fix]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error PASSED
```

* **Silent Mode (`verbose=False` - Compact Production Run):**

```text
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error PASSED

```

[▲ Back to Top](#-assert_exception_function)

---

### Case 2: Parameterized Test with Happy Path Verification (`valid_params`)

This function validates an internal configuration cache. 
It only accepts an empty dictionary `{}` (which acts as a cache reset). 
Any other input must trigger a framework exception.

```python
def validate_dynamic_cls_cache(value: Any) -> None:
    """Verifies that the configuration value is an empty dictionary — reserved for cache resets."""
    if value != {}:
        raise SimpleExceptionSettingsError(
            value=value,
            label="_dynamic_cls_cache",
            expected="an empty dict {} — for configuration and state reset routines only",
            problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
            how_to_fix=(
                "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
                "To clear this cache manually during hot-reloads or tests, assign an empty dict: SimpleExceptionSettings._dynamic_cls_cache = {}",
            ),
        )
```

#### Test Suite Implementation

We can leverage `pytest.mark.parametrize` to sweep across multiple malformed types 
(strings, integers, non-empty structures) while passing `valid_params=({},)` 
in every execution to guarantee that valid cache resets never accidentally break.

```python
@pytest.mark.parametrize("invalid_value", [
    "bad-value",            # String type
    123,                    # Integer type
    (),                     # Empty tuple
    [],                     # Empty list
    {"cached_key": str},    # Non-empty dictionary (unauthorized modification attempt)
])
def test_validate_dynamic_cls_cache(subtests, invalid_value):
    """Ensure that all invalid inputs raise a guard exception while the valid input passes cleanly."""
    assert_exception_function(
        subtests,
        validate_dynamic_cls_cache,
        invalid_params=(invalid_value,),
        valid_params=({},),  # Audits positive execution pass (Happy Path)
        exception_type=SimpleExceptionSettingsError,
        value=invalid_value,
        label="_dynamic_cls_cache",
        expected="an empty dict {} — for configuration and state reset routines only",
        problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
        how_to_fix=(
            "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
            "To clear this cache manually during hot-reloads or tests, assign an empty dict: SimpleExceptionSettings._dynamic_cls_cache = {}",
        ),
    )
```

[▲ Back to Top](#-assert_exception_function)

---

### Case 3: Decoupled Positive Path Sweeps and Target Failures

Consider a complex validation utility that guards a system blacklist. 
The blacklist must be a `tuple` containing exclusively string elements. 
This utility raises two different error patterns: one if the container type is wrong, 
and another if an invalid element type is detected inside it.

```python
def validate_location_blacklist(value: Any) -> None:
    """Verifies that the supplied value is a tuple containing only string elements."""
    # 1. Audit the baseline container type
    if not isinstance(value, tuple):
        raise SimpleExceptionSettingsError(
            value=value,
            label="LOCATION_BLACKLIST",
            expected="tuple[str, ...] — a tuple of strings containing filename patterns",
            problem="value is not a tuple",
            how_to_fix=(
                "Wrap the value in a tuple: ('filename.py',)",
                "To set an empty blacklist use an empty tuple: ()",
            ),
        )

    # 2. Audit individual element types
    bad_items = [i for i in value if not isinstance(i, str)]
    if bad_items:
        raise SimpleExceptionSettingsError(
            value=bad_items,
            label="LOCATION_BLACKLIST",
            expected="a tuple containing only string elements",
            problem=f"tuple contains invalid non-string elements (found {len(bad_items)} invalid item(s))",
            how_to_fix=(
                "Check all items — each one must be a string (str).",
                "Each item defines a file name pattern that will be skipped during location resolution.",
            ),
        )
```

#### Test Suite Implementation

Here is how we decouple happy-path validation sweeps from a target container structural audit:

```python
# 1. Parameterized sweep for happy paths (Valid inputs)
@pytest.mark.parametrize("valid_input", [
    (),                               # Empty blacklist
    ("a.py", "b.py"),                 # Populated blacklist
    ("single_element.py",),           # Single-element blacklist
])
def test_validate_location_blacklist_valid_input(subtests, valid_input):
    """Verify that the validator allows compliant tuple layouts to pass cleanly."""
    assert_function_valid_input(
        subtests,
        validate_location_blacklist,
        valid_params=(valid_input,),  # Unpacked as positional argument
        verbose=False
    )

# 2. Parameterized sweep for bad containers (Invalid inputs)
@pytest.mark.parametrize("invalid_container", [
    ["a.py", "b.py"],                 # List layout (invalid)
    "a.py",                           # Raw string (invalid)
    123,                              # Integer (invalid)
    {"a.py", "b.py"},                 # Set container (invalid)
    {"key": "value"},                 # Dictionary mapping (invalid)
])
def test_validate_location_blacklist_invalid_container(subtests, invalid_container):
    """Verify that non-tuple inputs trigger a container-level diagnostic exception."""
    assert_exception_function(
        subtests,
        validate_location_blacklist,
        invalid_params=(invalid_container,),
        valid_params=((),),                   # Reference happy-path baseline (empty tuple)
        exception_type=SimpleExceptionSettingsError,
        value=invalid_container,
        label="LOCATION_BLACKLIST",
        expected="tuple[str, ...] — a tuple of strings containing filename patterns",
        problem="value is not a tuple",
        how_to_fix=(
            "Wrap the value in a tuple: ('filename.py',)",
            "To set an empty blacklist use an empty tuple: ()",
        ),
    )
```

[▲ Back to Top](#-assert_exception_function)

---

[⬅️ Back to README_TESTING](../README_TESTING.md)  
[⬅️ Back to README](../../../README.md)