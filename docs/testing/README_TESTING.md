# 📦 `simplibs.exception.testing`

**Unified Testing Framework for SimpleException**

The `testing` package provides a comprehensive, modular, and automated infrastructure for validating:

* **Exceptions** (structural integrity, inheritance, constructors, and public APIs).
* **Callables & Functions** that raise these target exceptions.
* **Complex Test Scenarios** with exhaustive parameter variations.
* **Entire Subsystems** simultaneously using automated testing matrices.

This represents the highest abstraction layer of the `SimpleException` testing 
architecture—engineered to be deterministic, highly readable, easily extensible, 
CI/CD-ready, and above all, **completely free of duplicate boilerplate code**.

---

## ⚙️ Architectural Role of the Package

The `testing` package functions as a **complete, self-contained testing framework** organized into layers:

* **Low-Level Asserts** ➔ Atomic validations acting as the fundamental building blocks.
* **Orchestrators** ➔ Facade patterns executing sequential multi-phase verification pipelines.
* **Bulk Test Suite** ➔ Automated matrix-driven test suites to sweep entire components.
* **Tools** ➔ Unified semantic wrappers and context managers for robust subtest control.

---

## 🧭 Package Directory Layout

### `testing (root)`

**Composite Orchestrators for Complete Test Scenarios**

These components unify low-level atomic assertions into seamless, 
sequential testing pipelines using the **Facade** pattern.

Includes:

* `assert_exception_class` — Runs comprehensive structural and behavioral 
compliance audits on exception blueprints.
* `assert_exception_function` — Orchestrates functional logic execution and telemetry checks.

➡️ [README_CLASS](orchestrators/README_CLASS.md)  
➡️ [README_FUNCTION](orchestrators/README_FUNCTION.md)  

---

### `testing/asserts`

**Low-Level Atomic Validation Utilities**

Atomic assertions that serve as the precise execution engines underneath the entire framework.

* **`asserts/classes` — Class Blueprint Validation**
* `assert_class_inheritance` — Verifies inheritance hierarchies.
* `assert_class_defaults` — Validates class-level metadata defaults.
* `assert_class_constructor` — Audits instantiation, keyword propagation, and fallback flows.
* `assert_class_interface` — Checks public APIs, serialization methods, and dunder behaviors.


* **`asserts/functions` — Functional Execution Validation**
* `assert_function_callable` — Ensures the target object is executable.
* `assert_function_valid_input` — Runs happy-path trial executions (must complete without raising exceptions).
* `assert_function_raises` — Intercepts execution failures and validates the raised exception class.


* **`asserts/fields` — Telemetry Attribute Validation**
* `assert_exception_fields` — Performs detailed compliance sweeps across individual diagnostic properties.

➡️ [README_ASSERTS_CLASS](asserts/README_ASSERTS_CLASS.md)  
➡️ [README_ASSERTS_FUNCTIONS](asserts/README_ASSERTS_FUNCTIONS.md)  
➡️ [README_ASSERTS_FIELDS](asserts/README_ASSERTS_FIELDS.md)  

---

### `testing/bulk_test`

**Automated Subsystem Matrix Orchestration**

The absolute highest testing layer. It enables developers to define 
complete architectural subsystem sweeps using a single declarative data matrix.

* Automatically detects the structural signature footprint of each registered item.
* Routes items dynamically to their correct specialized validation engines.
* Supports both rapid shallow smoke checks and deep architectural audits.
* Minimizes boilerplate, allowing a single master test case to validate dozens of distinct components.

Includes:

* `exceptions_bulk_test` — The primary matrix execution engine and router.
* `FuncCase` — A declarative data container representing an isolated, multi-field test scenario.

➡️ [README_BULK_TEST](orchestrators/README_BULK_TEST.md)  
➡️ [README_FUNC_CASE](tools/README_FUNC_CASE.md)  

---

### `testing/tools`

**Framework-Wide Testing Utilities**

Helper utilities that simplify subtest boundary controls and guarantee parameter type safety.

Includes:

* `Kwargs` — A semantic type wrapper that explicitly distinguishes packed 
keyword arguments from standard dictionaries.
* `maybe_subtest` — A unified context manager to gracefully handle conditional pytest subtest execution.

➡️ [README_KWARGS](tools/README_KWARGS.md)  
➡️ [README_MAYBE_SUBSET](tools/README_MAYBE_SUBSET.md)  

[▲ Back to Top](#-simplibsexceptiontesting)

---

[⬅️ Back to README](../../README.md)