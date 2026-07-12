# 📦 `testing/tools` — Utility Tools for Structured Test Pipelines

Balíček `testing/tools` obsahuje malé, vysoce zaměřené pomocné nástroje používané napříč testovacími moduly knihovny **SimpleException**.  
Je navržen tak, aby poskytoval:

- **jednotné API**,  
- **jasné chování**,  
- **bezpečné guardy**,  
- **čitelné testovací výpisy**,  
- **nulovou syntaktickou zátěž** pro testovací kód.

Tyto nástroje nejsou určeny pro koncové uživatele knihovny — jsou určeny výhradně pro interní testování a pro vývojáře, kteří chtějí psát testy konzistentně s architekturou knihovny.

---

## 🧭 Co tento balíček řeší?

### 1) Rozlišování mezi dict a kwargs (`Kwargs`)
V Pythonu je běžné, že:

- `{...}` může být buď **hodnota**, nebo **kwargs**.  
- V testovacích pipelines je potřeba tyto dvě věci **jednoznačně odlišit**.

Třída `Kwargs` řeší přesně tento problém:

- umožňuje předat kwargs explicitně,  
- zabraňuje nechtěné interpretaci dictu jako hodnoty,  
- poskytuje bezpečný, neměnný wrapper,  
- podporuje jak `Kwargs(a=1, b=2)`, tak `Kwargs({"a": 1})`.

---

### 2) Podmíněné subtesty (`maybe_subtest`)
Testovací pipeline knihovny používá `pytest-subtests` pro:

- oddělení jednotlivých validačních kroků,  
- čitelné výpisy,  
- izolaci chyb.

Ale ne vždy je žádoucí subtesty aktivovat — například:

- při rychlém CI běhu,  
- při tichém režimu,  
- při kompozitních testech.

`maybe_subtest` řeší tento problém:

- pokud `verbose=True` → vytvoří subtest blok,  
- pokud `verbose=False` → chová se jako no-op context manager.

Díky tomu testovací kód nemusí obsahovat žádné podmínky typu:

```python
if verbose:
    with subtests.test(...):
        ...
else:
    ...
```

---

## 📁 Obsah balíčku

### `Kwargs.py`
Neměnný wrapper pro předávání keyword argumentů.

Poskytuje:

- bezpečnou inicializaci,  
- validaci přes `raise_unsupported_kwargs_parameter`,  
- dictionary-like API (`Mapping`),  
- podporu pro `**Kwargs(...)`.

---

### `maybe_subtest.py`
Podmíněný context manager pro subtesty.

Poskytuje:

- izolované subtesty v verbose režimu,  
- nulovou režii v silent režimu,  
- jednotné API pro všechny testy.

---

### `_validations/raise_unsupported_kwargs_parameter.py`
Interní guard, který:

- detekuje neplatné inicializace `Kwargs`,  
- poskytuje strukturované chyby přes `SimpleExceptionSettingsError`,  
- zajišťuje, že testovací pipeline nikdy nepracuje s nevalidními daty.

---

## 🔍 Příklady použití

### Použití `Kwargs`
```python
def func(**kwargs):
    return kwargs

assert func(**Kwargs(timeout=10, strict=True)) == {"timeout": 10, "strict": True}
```

### Použití `maybe_subtest`
```python
with maybe_subtest(subtests, name="constructor", verbose=True):
    assert exc.message == "Boom"
```

### Silent režim
```python
with maybe_subtest(subtests, name="constructor", verbose=False):
    assert exc.message == "Boom"
```

---

## 🛡️ Architektonické principy

- **Jednoznačnost**  
  `Kwargs` odstraňuje typovou nejednoznačnost mezi dict a kwargs.

- **Bezpečnost**  
  Guard funkce zajišťuje, že testy nikdy nepracují s nevalidními daty.

- **Čistota testů**  
  `maybe_subtest` eliminuje podmínky v testovacím kódu.

- **Neměnnost**  
  `Kwargs` je frozen → žádné mutace, žádné vedlejší efekty.

- **Konzistence**  
  Všechny testy knihovny používají stejné nástroje, stejné API, stejný styl.

---
