# 📦 `simplibs.exception.testing` — Unified Testing Framework for SimpleException

Balíček `testing` poskytuje kompletní, modulární a automatizovanou infrastrukturu pro testování:

- **výjimek** (jejich struktury, dědičnosti, konstruktoru, API),  
- **funkcí**, které výjimky vyvolávají,  
- **komplexních testovacích scénářů**,  
- **celých subsystémů** pomocí automatizovaných testovacích matic.

Je to nejvyšší vrstva testovací architektury SimpleException — navržená tak, aby byla:

- deterministická,  
- čitelná,  
- snadno rozšiřitelná,  
- vhodná pro CI/CD,  
- a především **bez duplicitního kódu**.

---

## 🧭 Struktura balíčku

### 📁 `asserts`
Sada nízkoúrovňových validačních nástrojů pro:

- **třídy výjimek** (`asserts/classes`)  
- **diagnostická pole výjimek** (`asserts/fields`)  
- **funkce a jejich chování** (`asserts/functions`)

Každý subbalíček má vlastní API a vlastní README.

📄 **Více informací:**  
→ *viz* `asserts/README.md`  
**asserts**

---

### 📁 `asserts/classes`
Validace struktury výjimek:

- dědičnost,  
- defaulty,  
- konstruktor,  
- public API.

📄 **Více informací:**  
→ *viz* `asserts/classes/README.md`  
**asserts/classes**

---

### 📁 `asserts/fields`
Validace jednotlivých diagnostických atributů výjimek:

- message,  
- error_name,  
- expected,  
- value,  
- problem,  
- context,  
- how_to_fix,  
- location metadata.

📄 **Více informací:**  
→ *viz* `asserts/fields/README.md`  
**asserts/fields**

---

### 📁 `asserts/functions`
Validace funkční logiky:

- callable gate,  
- valid input,  
- invalid input + typ výjimky,  
- parametrická normalizace (`manage_param`).

📄 **Více informací:**  
→ *viz* `asserts/functions/README.md`  
**asserts/functions**

---

### 📁 `bulk_test`
Automatizovaný orchestrátor pro testovací matice:

- rozpozná typ položky,  
- směruje ji do správného validačního modulu,  
- podporuje shallow i deep režim,  
- umožňuje psát jediný test pokrývající celý subsystém.

Obsahuje:

- `exceptions_bulk_test` — hlavní orchestrátor  
- `FunctionCase` — deklarativní scénáře  
- `_utils` — introspekční pomocníci

📄 **Více informací:**  
→ *viz* `bulk_test/README.md`  
**bulk_test**

---

### 📁 `tools`
Pomocné nástroje používané napříč celou testing vrstvou:

- `Kwargs` — bezpečný wrapper pro keyword argumenty  
- `maybe_subtest` — jednotné řízení subtestů  
- `_validations` — interní pomocné funkce

📄 **Více informací:**  
→ *viz* `tools/README.md`  
**tools**

---

### 📄 Orchestrátory nejvyšší úrovně

#### `assert_exception_class.py`
Kompozitní orchestrátor pro testování výjimek.

📄 **Více informací:**  
→ *viz* `README_CLASS.md`  
**assert_exception_class**

#### `assert_exception_function.py`
Kompozitní orchestrátor pro testování funkcí vyvolávajících výjimky.

📄 **Více informací:**  
→ *viz* `README_FUNCTION.md`  
**assert_exception_function**

---

## 🧩 Architektonická role balíčku

Balíček `testing` je navržen jako **kompletní testovací framework** pro SimpleException:

- nízkoúrovňové asserts → atomické testy,  
- orchestrátory → kompozitní testy,  
- bulk test → automatizované matice,  
- tools → jednotné API pro subtesty a parametry.

Díky tomu lze psát testy, které jsou:

- krátké,  
- přehledné,  
- bez duplicit,  
- snadno udržovatelné,  
- vhodné pro CI/CD.

---
