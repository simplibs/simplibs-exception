# 📦 `simplibs.exception.testing` 
**Unified Testing Framework for SimpleException**

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

## ⚙️ Architektonická role balíčku

Balíček `testing` je navržen jako **kompletní testovací framework** pro SimpleException:

- **nízkoúrovňové asserts** → atomické testy,  
- **orchestrátory** → kompozitní testy,  
- **bulk test** → automatizované matice,  
- **tools** → jednotné API pro subtesty a parametry.


---

## 🧭 Struktura balíčku

### `testing (root)`
**Kompozitní orchestrátory pro kompletní testovací scénář**

Sjednocují nízkoúrovňové testy do ucelených, sekvenčních testovacích pipeline (vzor Facade).

Obsahuje:
- `assert_exception_class` — pro komplexní audit tříd výjimek  
- `assert_exception_function` — pro testování funkcí vyvolávajících výjimky  

📄 **Více informací:**  
→ [README_CLASS](__doc/orchestrators/README_CLASS.md)  
→ [README_FUNCTION](__doc/orchestrators/README_FUNCTION.md)  


---

### `testing/asserts`
**Sada nízkoúrovňových validačních nástrojů**

Atomické testy, které tvoří základní stavební kameny celého testovacího frameworku.

* **`asserts/classes` — validace struktury třídy**
    * `assert_class_inheritance` — ověří předky třídy
    * `assert_class_defaults` — ověří defaultní hodnoty zapsané na třídě
    * `assert_class_constructor` — ověří nativní konstrukci a propagaci parametrů
    * `assert_class_interface` — ověří veřejné API a dunder metody
* **`asserts/functions` — validace funkční logiky**
    * `assert_function_callable` — ověří, zda je testovaný objekt volatelný
    * `assert_function_valid_input` — ověří pozitivní průchod (nesmí se vyvolat výjimka)
    * `assert_function_raises` — ověří záchyt a typ vyvolané výjimky
* **`asserts/fields` — validace diagnostických polí**
    * `assert_exception_fields` — detailní audit jednotlivých atributů zachycené výjimky

📄 **Více informací:**  
→ [README_ASSERTS_CLASS](__doc/asserts/README_ASSERTS_CLASS.md)  
→ [README_ASSERTS_FUNCTIONS](__doc/asserts/README_ASSERTS_FUNCTIONS.md)  
→ [README_ASSERTS_FIELDS](__doc/asserts/README_ASSERTS_FIELDS.md)  


---

### `testing/bulk_test`
**Automatizovaný orchestrátor pro testovací matice**

Nejvyšší vrstva frameworku. Umožňuje definovat test celého subsystému formou jediné, přehledné datové tabulky.

- rozpozná typ vložené položky,  
- směruje ji automaticky do správného validačního modulu,  
- podporuje shallow i deep režim,  
- umožňuje psát jediný test pokrývající desítky komponent najednou.

Obsahuje:
- `exceptions_bulk_test` — hlavní maticový runner a router  
- `FuncCase` — deklarativní datový kontejner pro popis jednoho testovacího scénáře  

📄 **Více informací:**  
→ [README_BULK_TEST](__doc/orchestrators/README_BULK_TEST.md)  
→ [README_FUNC_CASE](__doc/tools/README_FUNC_CASE.md)  

---

### `testing/tools`
**Pomocné nástroje používané napříč celou testing vrstvou**

Utility, které zjednodušují práci se subtesty a zajišťují typovou čistotu parametrů.

Obsahuje:
- `Kwargs` — bezpečný sémantický wrapper pro keyword argumenty (odlišuje je od běžného slovníku)  
- `maybe_subtest` — jednotný context manager pro podmíněné řízení a zapínání pytest subtestů  

📄 **Více informací:**  
→ [README_KWARGS](__doc/tools/README_KWARGS.md)  
→ [README_MAYBE_SUBSET](__doc/tools/README_MAYBE_SUBSET.md)  

---