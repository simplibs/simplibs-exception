# 📦 Custom Presentation Modes

**Designing Tailor-Made Visual Engines for SimpleException**

If none of the four pre-packaged presentation modes satisfy your requirements, 
`SimpleException` grants you complete architectural freedom to construct your own custom visual styles. 
This is particularly useful for integrating with proprietary enterprise CLI tools, 
specialized logging infrastructures, or third-party terminal formatting libraries.

> 🧭 **Table of Contents:**
> * [⚙️ Architectural Foundation: ModeBase](#-architectural-foundation-modebase)
> * [🔑 The SimpleExceptionData Interface](#-the-simpleexceptiondata-interface)
> * [🖨️ Helper Formatting Printers](#-helper-formatting-printers)
> * [📏 Formatting Layout Constants](#-formatting-layout-constants)
> * [📖 Real-World Implementations](#-real-world-implementations)

---

## ⚙️ Architectural Foundation: `ModeBase`

The foundation of every presentation mode is the `ModeBase` Abstract Base Class (ABC). 
It establishes a rigid, clean interface using the **Template Method** design pattern:

* **Abstract Internal Method `_render` (Mandatory Override):** 
Contains your custom formatting and layout pipeline. 
It accepts a data container satisfying `SimpleExceptionDataProtocol` 
and must return the final formatted string (`str`).
* **Public Method `render` (Never Override):** 
Serves as the immutable public entry point. 
* The framework invokes this method automatically during exception processing 
to handle validation checks before dispatching to your custom SPI.

---

## 🔑 The `SimpleExceptionData` Interface

When implementing your custom `_render` method, you have access to the complete, 
immutable state of the raised exception encapsulated inside the `SimpleExceptionData` container.

### 🔬 Lazy Evaluation & Location Metadata (`caller_info`)

Instead of performing expensive stack trace traversals inside the active exception lifecycle, 
`SimpleExceptionData` delegates frame detection to a lazy-evaluated property named `caller_info`:

1. **Lazy Execution:** 
Scanning the execution stack trace occurs **only** when your presentation mode 
explicitly requests it (by accessing `data.caller_info`). 
If your mode does not output location metadata, the performance overhead is exactly zero.
2. **Defensive Caching:** 
Once resolved, the framework locks the resulting metadata dictionary inside an internal cache. 
Subsequent access is instantaneous.
3. **Structured Payload:** 
The `caller_info` property returns either `None` (if location tracking is disabled or resolution failed) 
or a structured dictionary (`dict[str, Any]`) containing **four key components**:
   * **`file`** ➔ The short file name (e.g., `service.py`).
   * **`path`** ➔ The absolute system path to the source file.
   * **`line`** ➔ The exact line number (`int`) where the exception was raised.
   * **`function`** ➔ The name of the function or method that triggered the failure.



### 📋 Exception State Attribute Matrix

You can read and format the following public attributes inside your custom `_render` method:

#### Core Metadata

| Attribute                  | Default Value | Description                                                                                       |
| :------------------------- | :------------ | :------------------------------------------------------------------------------------------------ |
| `error_name`               | `"ERROR"`     | The primary exception category, typically printed in the header banner.                           |
| `exception`                | `None`        | Reference to the actual exception class to preserve inheritance checks.                           |
| `intercepted_exception`     | `None`        | A text representation of a caught underlying exception from a `try-except` block.                 |

#### Inspected Payload

| Attribute | Default Value | Description                                                                                                    |
| :-------- | :------------ | :------------------------------------------------------------------------------------------------------------- |
| `value`   | `UNSET`       | The active runtime object that failed validation. Safely supports `None` (distinguished via the `UNSET` token). |

#### Diagnostic Descriptions

| Attribute      | Default Value | Description                                                                                              |
| :------------- | :------------ | :------------------------------------------------------------------------------------------------------- |
| `label`        | `None`        | Contextual label identifying the inspected payload (e.g., `"user_id"`).                                 |
| `expected`     | `None`        | Description of the anticipated state or validation threshold.                                           |
| `problem`      | `None`        | Explanation of what failed. Supports flat `str` or a `tuple[str, ...]` for multi-line details.           |
| `context`      | `None`        | Supplementary environment metadata (IPs, request IDs, hashes). Supports `str` or `tuple[str, ...]`.     |
| `message`      | `None`        | Traditional free-text error message. If populated, it can bridge other granular fields.               |

#### Actionable Remediation

| Attribute     | Default Value | Description                                                                                             |
| :------------ | :------------ | :------------------------------------------------------------------------------------------------------ |
| `how_to_fix`  | `None`        | Actionable steps to mitigate the issue. Automatically formatted as a checklist. Supports `str` or `tuple[str, ...]`. |

[🔼 Back to Top](#-custom-presentation-modes)

---

## 🖨️ Helper Formatting Printers

To streamline custom layout construction, `SimpleException` exposes a rich suite 
of low-level printing utilities. Their use is optional but highly recommended 
to maintain layout alignment, auto-wrap long text payloads, and standardize output across your codebase.

All printers share a consistent, defensive safety contract: **If the target input value is empty, 
omitted, or equals `UNSET`/`None`, the printer immediately and safely returns `None`.** 
This allows you to chain multiple printers in a clean list and filter out unpopulated lines dynamically 
via Python's `" \n".join()` method.

---

### `print_intro`

Renders the primary exception identifier, merging the core error name with an optional localized label.

```python
def print_intro(
    error_name: str,
    label: str | None,
    *,
    prefix: str = "⚠️ ",
    _log_mode: bool = False
) -> str
```

* **Standard Mode:** `<PREFIX><ERROR_NAME>[: <LABEL>]`

```text
⚠️ VALUE_ERROR
⚠️ VALUE_ERROR: Invalid email format
```

* **Log Mode (`_log_mode=True`):** `error='<ERROR_NAME>'[ label='<LABEL>']`

```text
error='VALUE_ERROR'
error='VALUE_ERROR' label='Invalid email format'
```

---

### `print_message`

Outputs the developer-facing custom description string.

```python
def print_message(
    message: str | None,
    *,
    prefix: str = "Message:   ",
    _log_mode: bool = False
) -> str | None
```

* **Standard Mode:**

```text
Message:   The requested user ID was not found in the database.
```

* **Log Mode (`_log_mode=True`):**

```text
message='The requested user ID was not found in the database.'
```

---

### `print_value_with_type`

Displays the active runtime value coupled with its type wrapper. 
It features an automated truncation engine to prevent long serialized strings 
or objects from bloating the console.

```python
def print_value_with_type(
    value: Any,
    max_length: int | None = None,
    *,
    prefix: str = "Got:       ",
    _log_mode: bool = False
) -> str | None
```

* **Standard Mode:**

```text
Got:       'short string' (str)
Got:       'this is a very long string that will be... [truncated, 15 chars]' (str)
```

* **Log Mode (`_log_mode=True`):**

```text
value='short string' type=str
value="'this is a very long string that will be... [truncated, 15 chars]'" type=str
```

---

### `print_expected`

Renders the boundary conditions or value schemas that the system originally expected.

```python
def print_expected(
    expected: str | None,
    *,
    prefix: str = "Expected:  ",
    _log_mode: bool = False
) -> str | None
```

* **Standard Mode:**

```text
Expected:  a positive integer greater than 0
```

* **Log Mode (`_log_mode=True`):**

```text
expected='a positive integer greater than 0'
```

---

### `print_problem`

Renders detailed explanation statements. Natively handles both primitive strings and multi-line tuples.

```python
def print_problem(
    problem: tuple[str, ...] | str | None,
    *,
    prefix: str = "Problem:   ",
    _log_mode: bool = False,
    _oneline: bool = False
) -> str | None
```

* **Standard Mode (Vertical Multi-line):**

```text
Problem:   The database connection timed out after 5 seconds.
           Please check your network configuration and try again.
```

* **Oneline Mode (`_oneline=True`):**

```text
Problem:   The database connection timed out after 5 seconds. Please check your network configuration and try again.
```

* **Log Mode (`_log_mode=True`):**

```text
problem='The database connection timed out after 5 seconds. Please check your network configuration and try again.'
```

---

### `print_context`

Displays environmental context metadata.

```python
def print_context(
    context: tuple[str, ...] | str | None,
    *,
    prefix: str = "Context:   ",
    _log_mode: bool = False,
    _oneline: bool = False
) -> str | None
```

* **Standard Mode (Vertical Multi-line):**

```text
Context:   Occurred during the batch migration of user profiles.
           Processing record chunk #42 (items 4200-4300).
```

* **Oneline Mode (`_oneline=True`):**

```text
Context:   Occurred during the batch migration of user profiles. Processing record chunk #42 (items 4200-4300).
```

* **Log Mode (`_log_mode=True`):**

```text
context='Occurred during the batch migration of user profiles. Processing record chunk #42 (items 4200-4300).'
```

---

### `print_file_info`

Outputs location tracking metadata (file, line number, and function execution hook).

```python
def print_file_info(
    caller_info: dict | None,
    *,
    prefix: str = "File info: ",
    _log_mode: bool = False
) -> str | None
```

* **Standard Mode:**

```text
File info: src/auth/service.py | line: 42 | function: login_user
```

* **Log Mode (`_log_mode=True`):**

```text
file='src/auth/service.py' line=42 function='login_user'
```

---

### `print_file_path`

Renders the absolute physical filesystem path of the source file.

```python
def print_file_path(
    caller_info: dict | None,
    *,
    prefix: str = "File path: ",
    _log_mode: bool = False
) -> str | None
```

* **Standard Mode:**

```text
File path: /home/user/project/src/auth/service.py
```

* **Log Mode (`_log_mode=True`):**

```text
path='/home/user/project/src/auth/service.py'
```

---

### `print_how_to_fix`

Formats actionable mitigation procedures into an obvious troubleshooting checklist.

```python
def print_how_to_fix(
    how_to_fix: tuple[str, ...] | str | None,
    *,
    prefix: str = "🔧 How to fix:",
    _log_mode: bool = False,
    _oneline: bool = False
) -> str | None
```

* **Standard Checklist Mode:**

```text
🔧 How to fix:
     • Ensure the input field enforces front-end email format filtering.
     • Check the downstream gateway router payload parser encoding schema.
```

* **Oneline Mode (`_oneline=True`):**

```text
🔧 How to fix: Ensure the input field enforces front-end email format filtering. Check the downstream gateway...
```

* **Log Mode (`_log_mode=True`):**

```text
how_to_fix='Ensure the input field enforces front-end email format filtering. Check the downstream gateway...'
```

---

### `print_intercepted_exception`

Exposes caught underlying exceptions extracted from `try-except` blocks.

```python
def print_intercepted_exception(
    exception: Any,
    *,
    prefix: str = "Intercepted exception",
    _log_mode: bool = False,
    _oneline: bool = False
) -> str | None
```

* **Standard Mode:**

```text
Intercepted exception (ValueError):
    Expecting value: line 1 column 1 (char 0)
```

* **Oneline Mode (`_oneline=True`):**

```text
Intercepted exception (ValueError): Expecting value: line 1 column 1 (char 0)
```

* **Log Mode (`_log_mode=True`):**

```text
intercepted_exception='ValueError'
```

[🔼 Back to Top](#-custom-presentation-modes)

---

## 📏 Formatting Layout Constants

These typographical constants ensure strict pixel-perfect vertical alignment and uniform segment separation.

---

### `DOUBLE_LINE`

Primary layout frame boundary.

* **Value:** `═` * 65
* **Purpose:** Establishes major layout framing. Placed at the absolute header 
and footer boundaries of `PRETTY` panels.

---

### `SINGLE_LINE`

Secondary layout divider.

* **Value:** `─` * 65
* **Purpose:** Logically separates internal data regions 
(specifically isolation of the `🔧 How to fix:` section).

---

### `EMPTY_PREFIX`

Multi-line margin alignment.

* **Value:** `"\n           "` (Newline followed by 11 padding spaces).
* **Purpose:** Forces subsequent rows of multi-line fields 
(e.g., `problem`, `context`) to form a perfectly aligned vertical column underneath 
their initial header prefixes (matching the 11-character width of labels like `Problem:   `).

---

### `DOT_PREFIX`

Checklist bullet layout.

* **Value:** `"\n     • "` (Newline, 5 padding spaces, and a bullet character).
* **Purpose:** Builds indented bullet lists specifically beneath the remediation header.

[🔼 Back to Top](#-custom-presentation-modes)

---

## 📖 Real-World Implementations

The cleanest way to grasp custom presentation engine design is to inspect the codebase 
of `SimpleException`'s native formats. All four standard modes are written declaratively 
using the standard helpers.

The central pattern is always the same: **collect all formatted line segments in a sequence, 
then join them with `\n` (or space) while filtering out `None` values.** 
This single pattern guarantees layout elasticity out of the box.

### 1. The `PRETTY` Implementation (`PrettyMessage`)

```python
class PrettyMessage(ModeBase):
    """Structured output framed with double lines — the default presentation mode."""

    def _render(
        self: "ModeBaseProtocol", data: "SimpleExceptionDataProtocol"
    ) -> str:
        location = data.caller_info

        # Check if we have any granular structured data for the inner body block
        has_details = any(
            [
                data.expected,
                data.value is not UNSET,
                data.problem,
                data.context,
            ]
        )

        lines = [
            # 1. Primary identification header (⚠️ ERROR_NAME: label)
            DOUBLE_LINE,
            print_intro(data.error_name, data.label),

            # 2. Render secondary line ONLY if granular structure details follow
            DOUBLE_LINE if has_details else None,

            # 3. Core body section (Printers return None internally if fields are omitted)
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value),
            print_problem(data.problem),
            print_context(data.context),

            # 4. Shared location metadata components
            print_file_info(location),
            print_file_path(location),

            # 5. Actionable remediation block (How to fix)
            SINGLE_LINE if data.how_to_fix else None,
            print_how_to_fix(data.how_to_fix),
            DOUBLE_LINE,

            # 6. Captured underlying exception block at the absolute bottom
            print_intercepted_exception(data.exception),
        ]

        return "\n".join(line for line in lines if line)
```

### 2. The `SIMPLE` Implementation (`SimpleMessage`)

```python
class SimpleMessage(ModeBase):
    """Output without decorative lines — plain text layout."""

    def _render(
        self: "ModeBaseProtocol", data: "SimpleExceptionDataProtocol"
    ) -> str:
        location = data.caller_info

        lines = [
            # 1. Primary identification header (⚠️ ERROR_NAME: label)
            print_intro(data.error_name, data.label),

            # 2. Core exception details (Printers return None if values are omitted)
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value),
            print_problem(data.problem),
            print_context(data.context),

            # 3. Shared location metadata components
            print_file_info(location),
            print_file_path(location),

            # 4. Actionable remediation block (How to fix)
            print_how_to_fix(data.how_to_fix),

            # 5. Captured underlying exception block at the absolute bottom
            print_intercepted_exception(data.exception),
        ]

        return "\n".join(line for line in lines if line)
```

### 3. The `ONELINE` Implementation (`OnelineMessage`)

```python
class OnelineMessage(ModeBase):
    """Compact single-line output for terminal use and rapid debugging cycles."""

    def _render(
        self: "ModeBaseProtocol", data: "SimpleExceptionDataProtocol"
    ) -> str:
        location = data.caller_info

        # Gather all formatted parts using standard human prefixes
        parts = [
            print_intro(data.error_name, data.label),
            print_message(data.message),
            print_expected(data.expected),
            print_value_with_type(data.value),
            print_problem(data.problem, _oneline=True),
            print_context(data.context, _oneline=True),
            print_file_info(location),
            print_file_path(location),
        ]

        # Join only existing segments with the pipe separator
        return " | ".join(part for part in parts if part).strip()
```

### 4. The `LOG` Implementation (`LogMessage`)

```python
class LogMessage(ModeBase):
    """Machine-readable key-value output adhering to the logfmt specification."""

    def _render(
        self: "ModeBaseProtocol", data: "SimpleExceptionDataProtocol"
    ) -> str:
        location = data.caller_info

        parts = [
            # 1. Primary identification header (error=... or error=... label=...)
            print_intro(data.error_name, data.label, _log_mode=True),

            # 2. Structured core attributes (Printers handle safe !r quoting natively)
            print_message(data.message, _log_mode=True),
            print_expected(data.expected, _log_mode=True),
            print_value_with_type(data.value, _log_mode=True),
            print_problem(data.problem, _log_mode=True),
            print_context(data.context, _log_mode=True),

            # 3. Location tracing metadata
            print_file_info(location, _log_mode=True),
            print_file_path(location, _log_mode=True),
        ]

        # Join only active tokens into a perfectly flat space-separated stream row
        return " ".join(part for part in parts if part)
```

[🔼 Back to Top](#-custom-presentation-modes)

---

[⬅️ Back to README](../../README.md)