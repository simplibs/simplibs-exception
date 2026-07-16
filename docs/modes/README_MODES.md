# 📦 Presentation Modes

**Unified Elastic Exception Visualization Engine for SimpleException**

Presentation modes represent the rendering layer that transforms raw, structured context 
from `SimpleExceptionData` into its final textual representation. 
By strictly decoupling the data model from the visual presentation, 
you gain absolute control over how errors are displayed across developer consoles, 
logging pipelines, and production monitoring stacks.

The library ships with **four built-in industrial presets** along with a robust, 
extensible architecture designed to easily construct your own custom visual styles tailored 
to your team's standards.

> 🧭 **Table of Contents:**
> * [⚙️ Architectural Concept & Elasticity](#-architectural-concept--elasticity)
> * [🗂️ Built-in Presentation Modes Overview](#-built-in-presentation-modes-overview)
> * [📊 Visual Templates & Output Examples](#-visual-templates--output-examples)
>   * [The PRETTY Mode](#the-pretty-mode)
>   * [The SIMPLE Mode](#the-simple-mode)
>   * [The ONELINE Mode](#the-oneline-mode)
>   * [The LOG Mode](#the-log-mode)

---

## ⚙️ Architectural Concept & Elasticity

All presentation modes interact exclusively with the unified interface of the `SimpleExceptionData` container. 
The final output layout adapts dynamically based entirely on the specific arguments you pass to the exception:

* **Elastic Layout Engine:** 
The renderer only draws lines and blocks for which the developer has explicitly provided runtime data. 
If optional fields (such as `problem`, `context`, or `how_to_fix`) are left unconfigured, 
the layout automatically shrinks, omitting empty spaces and internal framing dividers. 
This guarantees a polished, professional look without awkward gaps.
* **Zero-Argument Safety:** 
Exceptions are engineered to deliver a highly readable and diagnostic output even when raised 
without any custom parameters (e.g., `raise MyCustomException()`). 
This accelerates rapid prototyping; you do not need to supply descriptive text immediately, 
as the engine automatically falls back to isolating and rendering the exact file path 
and line location of the failure.
* **Semantic Alignment:** 
Every diagnostic field has a dedicated visual role inside the layout 
(utilizing distinct bullet prefixes such as `DOT_PREFIX` or `EMPTY_PREFIX`). 
This ensures that even arbitrary combinations of sparse fields remain perfectly 
aligned in your terminal output.

---

## 🗂️ Built-in Presentation Modes Overview

The library includes four production-ready presentation strategies, 
covering the entire application lifecycle from local offline debugging 
to distributed cloud container environments:

1. **`PRETTY` (Default)** 
Engineered for maximum human readability during local development. 
It frames diagnostics inside thick graphical borders (`DOUBLE_LINE`), structured indentations, 
and explicit headers. It is designed to immediately capture a developer's attention 
within a dense stream of terminal output.
2. **`SIMPLE`** 
Identical to the `PRETTY` mode in terms of structural elasticity and content, 
but completely strips away all decorative frame lines. It is ideal for minimal terminal configurations, 
standard output pipes, and minimalist command-line interfaces (CLI).
3. **`ONELINE`** 
A compact, highly dense single-line layout where all active exception properties 
are flattened and separated by a pipe character (`|`). It is optimized for interactive shells, 
rapid terminal debugging cycles, and high-speed exception streaming.
4. **`LOG`** 
A machine-readable format adhering to the industry-standard **logfmt** specification (`key='value'`). 
It completely eliminates vertical layouts, sanitizes spaces, and formats diagnostic tokens 
for seamless ingestion into centralized log management platforms 
(such as Datadog, Kibana, Loki, or AWS CloudWatch).

[🔼 Back to Top](#-presentation-modes)

---

## 📊 Visual Templates & Output Examples

The section below illustrates the exact rendering behavior of the four built-in modes 
across three distinct states of data populating.

### The `PRETTY` Mode

A dynamically adaptive, framed block explicitly optimized for the developer's console.

```text
1. Empty Call (Absolute Minimum):
═════════════════════════════════════════════════════════════════
⚠️ ERROR NAME
File info: main.py | line: 12 | function: run_pipeline
File path: /usr/app/src/main.py
═════════════════════════════════════════════════════════════════

2. Message-Only Layout:
═════════════════════════════════════════════════════════════════
⚠️ ERROR NAME
Message:   An unexpected database error occurred.
File info: main.py | line: 12 | function: run_pipeline
File path: /usr/app/src/main.py
═════════════════════════════════════════════════════════════════

3. Full Structured Layout:
═════════════════════════════════════════════════════════════════
⚠️ VALIDATION_ERROR: Request Payload Validation Failed
═════════════════════════════════════════════════════════════════
Message:   The submitted account configuration contains illegal data blocks.
Expected:  An active user payload containing a valid enterprise email layout.
Got:       {'email': 'bad_mail', 'tier': 'premium'} (dict)
Problem:   The provided email string does not contain an '@' sign symbol.
           Domain resolution check failed for host 'bad_mail'.
Context:   Client IP: 192.168.1.55
           Request ID: req-9942a-x
File info: validators.py | line: 204 | function: validate_email
File path: /usr/app/src/validators.py
─────────────────────────────────────────────────────────────────
🔧 How to fix:
     • Ensure the input field enforces front-end email format filtering.
     • Check the downstream gateway router payload parser encoding schema.
═════════════════════════════════════════════════════════════════
Intercepted exception (ValueError):
    String validation failed during schema extraction.
```

[🔼 Back to Top](#-presentation-modes)

---

### The `SIMPLE` Mode

A clean, plain text layout delivering identical structural content to `PRETTY` 
without decorative graphical lines.

```text
1. Empty Call (Absolute Minimum):
⚠️ ERROR NAME
File info: main.py | line: 12 | function: run_pipeline
File path: /usr/app/src/main.py

2. Message-Only Layout:
⚠️ ERROR NAME
Message:   An unexpected database error occurred.
File info: main.py | line: 12 | function: run_pipeline
File path: /usr/app/src/main.py

3. Full Structured Layout:
⚠️ VALIDATION_ERROR: Request Payload Validation Failed
Message:   The submitted account configuration contains illegal data blocks.
Expected:  An active user payload containing a valid enterprise email layout.
Got:       {'email': 'bad_mail', 'tier': 'premium'} (dict)
Problem:   The provided email string does not contain an '@' sign symbol.
           Domain resolution check failed for host 'bad_mail'.
Context:   Client IP: 192.168.1.55
           Request ID: req-9942a-x
File info: validators.py | line: 204 | function: validate_email
File path: /usr/app/src/validators.py
🔧 How to fix:
     • Ensure the input field enforces front-end email format filtering.
     • Check the downstream gateway router payload parser encoding schema.
Intercepted exception (ValueError):
    String validation failed during schema extraction.
```

[🔼 Back to Top](#-presentation-modes)

---

### The `ONELINE` Mode

A highly compact, single-row string separating available fields using pipe delimiters.

```text
1. Empty Call (Absolute Minimum):
⚠️ ERROR NAME | File info: main.py | line: 12 | function: run_pipeline | File path: /usr/app/src/main.py

2. Message-Only Layout:
⚠️ ERROR NAME | Message: An unexpected database error occurred. | File info: main.py | line: 12 | function: run_pipeline | File path: /usr/app/src/main.py

3. Full Structured Layout:
⚠️ VALIDATION_ERROR: Request Payload Validation Failed | Message: The submitted account configuration contains illegal data blocks. | Expected: An active user payload containing a valid enterprise email layout. | Got: {'email': 'bad_mail', 'tier': 'premium'} (dict) | Problem: The provided email string does not contain an '@' sign symbol. Domain resolution check failed for host 'bad_mail'. | Context: Client IP: 192.168.1.55 Request ID: req-9942a-x | File info: validators.py | line: 204 | function: validate_email | File path: /usr/app/src/validators.py
```

*Note: The descriptive step-by-step `how_to_fix` checklist and the raw multiline 
`intercepted_exception` stack trace are intentionally omitted from this format 
to preserve the strict, low-profile single-row footprint.*

[🔼 Back to Top](#-presentation-modes)

---

### The `LOG` Mode

A single-row, structured, key-value configuration conforming to standard **logfmt**. 
Quotes are applied safely to isolate multi-word parameter blocks.

```text
1. Empty Call (Absolute Minimum):
error='ERROR_NAME' file='main.py' line=12 function='run_pipeline' path='/usr/app/src/main.py'

2. Message-Only Layout:
error='ERROR_NAME' message='An unexpected database error occurred.' file='main.py' line=12 function='run_pipeline' path='/usr/app/src/main.py'

3. Full Structured Layout:
error='VALIDATION_ERROR' label='Request Payload Validation Failed' message='The submitted account configuration contains illegal data blocks.' expected='An active user payload containing a valid enterprise email layout.' value="{'email': 'bad_mail', 'tier': 'premium'}" type='dict' problem='The provided email string does not contain an \x27@\x27 sign symbol. Domain resolution check failed for host \x27bad_mail\x27.' context='Client IP: 192.168.1.55 Request ID: req-9942a-x' file='validators.py' line=204 function='validate_email' path='/usr/app/src/validators.py'
```

[🔼 Back to Top](#-presentation-modes)

---

[⬅️ Back to README](../../README.md)