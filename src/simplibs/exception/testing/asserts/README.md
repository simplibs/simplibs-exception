# 📦 `testing/asserts` — Unified Assertion Suite for Exception & Function Validation

Balíček `asserts` představuje kompletní sadu validačních nástrojů používaných v testovací infrastruktuře knihovny **SimpleException**.  
Je rozdělen do tří specializovaných subbalíčků:

- **asserts/classes** — validace struktury výjimek  
- **asserts/fields** — validace jednotlivých atributů výjimek  
- **asserts/functions** — validace funkční logiky a chování funkcí  

Každý subbalíček má vlastní interní API, vlastní testy a vlastní README.

---

## 🧭 Struktura balíčku

### 📁 `asserts/classes`
Validace **tříd výjimek** — jejich struktury, dědičnosti, defaultů, konstruktoru a public API.

Obsahuje čtyři klíčové asserts:

- `assert_class_inheritance`  
- `assert_class_defaults`  
- `assert_class_constructor`  
- `assert_class_interface`  

📄 **Více informací:**  
→ *viz* `asserts/classes/README.md`  
**asserts/classes**

---

### 📁 `asserts/fields`
Validace **jednotlivých atributů výjimek** — textových polí, kontextu, metadat, diagnostických zpráv.

Obsahuje:

- `assert_exception_fields`  
- `_utils/_normalize_value`  
- `_utils/compare_strings`  

📄 **Více informací:**  
→ *viz* `asserts/fields/README.md`  
**asserts/fields**

---

### 📁 `asserts/functions`
Validace **funkcí**, které pracují s výjimkami nebo jinou validační logikou.

Obsahuje:

- `assert_function_callable`  
- `assert_function_raises`  
- `assert_function_valid_input`  
- `_utils/process_params`  

📄 **Více informací:**  
→ *viz* `asserts/functions/README.md`  
**asserts/functions**

---

## 🧩 Architektonická role balíčku

Balíček `asserts` tvoří základní stavební kameny vyšších testovacích orchestrátorů:

- `assert_exception_class`  
- `assert_exception_function`  
- `bulk_test`  

Díky modulárnímu rozdělení:

- **každý subbalíček řeší jednu oblast**,  
- **každý assert je samostatný a snadno testovatelný**,  
- **orchestrátory mohou jednotlivé asserts skládat do komplexních validačních pipeline**.

---

