# 📦 `FuncCase`

**Comprehensive Functional Audit Blueprint for Bulk Testing**

`FuncCase` is a specialized **declarative data container** designed to describe a single, 
self-contained functional test scenario. Instead of writing imperative test logic (step-by-step instructions), 
`FuncCase` allows you to define **what** should be tested and **which** diagnostic telemetry fields 
are expected within the raised exception.

By completely decoupling the test scenario specification from its runtime execution parameters, 
`FuncCase` makes it trivial to organize, reuse, and dynamically dispatch test cases — either 
as isolated standalone tests or nested inside matrix-based suite orchestrators.

---

### ⚙️ Architectural Principles

* **Declarative Schema Design:** 
Replaces verbose imperative code ("how" to run assertions) with a predictable state mapping 
("what" is expected). This makes tests exceptionally readable, visual, and simple to maintain.
* **Type and Interface Integrity:** 
All parameters are strictly typed and map symmetrically to the attributes exposed 
by the **SimpleException** library family.
* **Dynamic Decoupling:** 
Isolates static blueprint expectations from dynamic execution variables 
(such as `verbose` or `exact_match`). These parameters are configured on-demand 
at the invocation boundary (via `.run_test` or during orchestrator execution).

---

## 🛠️ Configuration & Parameters

### Mandatory Attributes of `FuncCase`

* **`func`** (`Callable[..., Any]`) ➔ The target function or validation callable under test.
* **`exception_type`** (`type[BaseException]`) ➔ The expected class type of the raised exception.
* **`invalid_params`** (`tuple | Kwargs`) ➔ Malformed parameters engineered to trigger an execution failure.

### Optional Attributes of `FuncCase`

* **`valid_params`** (`tuple | Kwargs`) ➔ Default: `UNSET`. 
Clean nominal parameters expected to pass without raising errors (validates positive functional paths).
* **Telemetry Fields** 
(`error_name`, `label`, `message`, `expected`, `value`, `problem`, `context`, `how_to_fix`, 
`exception`, `get_location`, `skip_locations`, `oneline`) ➔ Default: `UNSET`. 
Expected property values populated inside the caught exception instance.

### Mandatory Parameters for `.run_test()` Method

* **`subtests`** (`Any`) ➔ The native pytest subtests fixture manager instance.

### Optional Parameters for `.run_test()` Method

* **`exact_match`** (`bool`) ➔ Default: `False`. 
Enforces strict textual equality checks (using the `==` operator) across string attributes.
* **`startswith`** (`bool`) ➔ Default: `False`. 
Validates that targeted exception string fields begin with the expected prefix.
* **`verbose`** (`bool`) ➔ Default: `True`. 
Isolates each individual telemetry property check into its own pytest subtest frame.
* **`intro`** (`str`) ➔ Default: `""`. 
Namespace prefix prepended to generated subtest names in the console.
* **`deep_check`** (`bool`) ➔ Default: `True`. 
If `False`, limits validation to the exception class type and skips the exhaustive telemetry fields check.

### Return Value of `.run_test()` Method

* **`BaseException`** ➔ The caught, instantiated live exception object, 
returned to support downstream fluid assertions.

---

## 🔍 Class Definition Blueprint

```python
@dataclass(slots=True, kw_only=True)
class FuncCase:

    # Mandatory Attributes
    func: Callable[..., Any]
    exception_type: type[BaseException]
    invalid_params: tuple[Any, ...] | Kwargs
    
    # Optional Attributes
    valid_params: tuple[Any, ...] | Kwargs | UnsetType = UNSET
    error_name: str | UnsetType = UNSET
    label: str | None | UnsetType = UNSET
    message: str | None | UnsetType = UNSET
    expected: str | None | UnsetType = UNSET
    value: Any = UNSET
    problem: str | tuple[str, ...] | None | UnsetType = UNSET
    context: str | tuple[str, ...] | None | UnsetType = UNSET
    how_to_fix: str | tuple[str, ...] | None | UnsetType = UNSET
    exception: Exception | type[Exception] | None | UnsetType = UNSET
    get_location: bool | int | UnsetType = UNSET
    skip_locations: tuple[str, ...] | UnsetType = UNSET
    oneline: bool | UnsetType = UNSET

    # Execution Gateway Method
    def run_test(
        self,
        subtests: Any,
        *,
        exact_match: bool = False,
        startswith: bool = False,
        verbose: bool = True,
        intro: str = "",
        deep_check: bool = True,
    ) -> BaseException:
        return assert_exception_function(
            subtests,
            self.func,
            valid_params=self.valid_params,
            invalid_params=self.invalid_params,
            exception_type=self.exception_type,
            error_name=self.error_name,
            label=self.label,
            message=self.message,
            expected=self.expected,
            value=self.value,
            problem=self.problem,
            context=self.context,
            how_to_fix=self.how_to_fix,
            exception=self.exception,
            get_location=self.get_location,
            skip_locations=self.skip_locations,
            oneline=self.oneline,
            exact_match=exact_match,
            startswith=startswith,
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )
```

---

## 📖 Usage Examples

### Declaring and Defining a `FuncCase`

A `FuncCase` instance bundles the target logic (`func`), inputs (both positive and negative), 
and the expected exception attributes into a unified, declarative blueprint:

```python
# Defining the test scenario as a clean data structure
validate_cache_case = FuncCase(
    func=validate_dynamic_cls_cache,             # Target logic boundary
    valid_params={},                             # Happy-path parameters (optional)
    invalid_params="abc",                        # Payload designed to force execution failure
    exception_type=SimpleExceptionSettingsError, # Expected exception class type

    # Declarative expectations (telemetry audit):
    error_name="SETTINGS ERROR",
    label="_dynamic_cls_cache",
    expected="an empty dict {}",
    value="abc",
    problem="the multi-inheritance class cache is handled internally...",
    how_to_fix="To wipe the framework runtime state safely, invoke..."
)
```

### Direct Standalone Scenario Execution

Although `FuncCase` is optimized for bulk test matrices, you can dispatch 
and run any scenario individually within pytest using the `.run_test()` interface:

```python
def test_cache_validation_standalone(subtests):
    # Execute the comprehensive testing pipeline (Callable -> Valid Input -> Exception -> Fields)
    exc_instance = validate_cache_case.run_test(
        subtests,
        verbose=True,      # Dispatches individual telemetry property checks to subtests
        deep_check=True,   # Triggers a deep field metadata audit
    )
    
    # The runner returns the caught live exception instance for downstream custom assertions
    assert exc_instance.custom_dynamic_property is None
```

[▲ Back to Top](#-funccase)

---

[⬅️ Back to README_TESTING](../README_TESTING.md)  
[⬅️ Back to README](../../../README.md)