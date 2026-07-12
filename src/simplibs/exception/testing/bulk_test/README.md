# 📦 `bulk_test` — Automated Matrix Testing for Exceptions & Functional Pipelines

Balíček `bulk_test` poskytuje **automatizovaný orchestrátor**, který umožňuje spouštět rozsáhlé testovací matice nad:

- výjimkami,  
- funkcemi vyvolávajícími výjimky,  
- komplexními scénáři popsanými pomocí `FunctionCase`.

Je to nejvyšší vrstva testovacího frameworku SimpleException — umožňuje psát **jediný test**, který pokryje celou architekturu.

---

## 🧭 Struktura balíčku

### 📁 `bulk_test/exceptions_bulk_test.py`
Hlavní orchestrátor, který umí automaticky rozpoznat tři typy položek:

- **FunctionCase** → komplexní funkční scénář  
- **exception class** → struktura výjimky  
- **tuple (exc_class, func, *params)** → inline funkční test  

Každý typ je automaticky směrován do správného validačního modulu.

📄 **Více informací:**  
→ *viz vnitřní dokumentace v souboru*  
**exceptions_bulk_test**

---

### 📁 `bulk_test/FunctionCase.py`
Deklarativní datová třída, která popisuje **kompletní funkční testovací scénář**:

- cílová funkce,  
- validní parametry,  
- invalidní parametry,  
- očekávaný typ výjimky,  
- očekávané diagnostické hodnoty.

Slouží jako stavební blok pro `exceptions_bulk_test`.

📄 **Více informací:**  
→ *viz vnitřní dokumentace v souboru*  
**FunctionCase**

---

### 📁 `bulk_test/_utils`
Pomocné introspekční nástroje:

- `is_exception_class` — rozpozná, zda je položka výjimková třída  
- `is_exception_function` — rozpozná tuple `(exc_class, func, *params)`  

Tyto utilitky umožňují orchestrátoru automaticky směrovat položky do správných validačních modulů.

📄 **Více informací:**  
→ *viz vnitřní dokumentace v souborech*  
**bulk_test/_utils**

---

## 🧩 Architektonická role balíčku

Balíček `bulk_test` je navržen jako **automatizační vrstva**, která:

- sjednocuje testování výjimek a funkcí,  
- eliminuje duplicitní testovací kód,  
- umožňuje psát testovací matice jako seznam položek,  
- poskytuje fail‑fast chování,  
- podporuje shallow i deep režim.

Je to ideální nástroj pro testování celých subsystémů:

```python
exceptions_bulk_test(
    subtests,
    items=[
        MyException,
        (MyException, validate_input, "bad"),
        FunctionCase(
            func=validate_input,
            invalid_param=("bad",),
            exception_type=MyException,
            message="Invalid input",
        )
    ],
    deep_check=True
)
```

---

## 🛡️ Architektonické principy

- **Automatické směrování**  
  Každá položka je automaticky rozpoznána a zpracována správným modulem.

- **Modularita**  
  Funkční scénáře (`FunctionCase`) a výjimkové scénáře jsou oddělené.

- **Determinismus**  
  Pipeline má pevně definované pořadí kroků.

- **Shallow / Deep režim**  
  Umožňuje rychlé CI běhy i detailní architektonické audity.

- **Čitelnost**  
  Testovací matice jsou krátké, přehledné a snadno udržovatelné.

---
