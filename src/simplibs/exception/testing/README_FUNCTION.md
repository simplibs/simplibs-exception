# 📦 `assert_exception_function` — Composite Functional Boundary Auditor

`assert_exception_function` je **hlavní orchestrátor** pro testování funkcí, které mají vyvolávat výjimky typu **SimpleException** nebo jiných frameworkových chyb.  
Je to jediný vstupní bod, který provádí kompletní audit funkční logiky:

- validace, že objekt je callable,  
- validace pozitivního scénáře (valid input),  
- validace negativního scénáře (invalid input),  
- validace typu výjimky,  
- validace všech diagnostických polí výjimky.

Tento modul implementuje **Facade Pattern** — sjednocuje tři dílčí asserts do jedné konzistentní pipeline:

- `assert_function_callable`  
- `assert_function_valid_input`  
- `assert_function_raises`  
- `assert_exception_fields`  

---

## 🧭 Účel modulu

`assert_exception_function` slouží jako:

- **master orchestrátor** pro testování funkcí, které mají vyvolávat výjimky,  
- **jednotný vstupní bod** pro všechny testy, které validují funkční chování,  
- **automatizovaný kontrolní mechanismus**, který zajišťuje, že funkce splňuje všechny architektonické požadavky,  
- **základní stavební kámen** pro `bulk_test` a další automatické testovací nástroje.

Je navržen tak, aby byl:

- deterministický,  
- fail‑fast,  
- modulární,  
- čitelný a přehledný,  
- snadno rozšiřitelný.

---

## 🔧 Pipeline kroků

Orchestrátor provádí čtyři kroky v přesně definovaném pořadí:

### 1) **Callable Gate**
```python
assert_function_callable(...)
```
Ověří, že objekt je skutečně callable.

---

### 2) **Valid Input Sanity Check** *(pokud je `valid_param` zadán)*
```python
assert_function_valid_input(...)
```
Ověří, že funkce:

- úspěšně zpracuje validní vstup,  
- nevyvolá žádnou výjimku,  
- není „permanentně rozbitá“.

---

### 3) **Negative Boundary Check**
```python
exc = assert_function_raises(...)
```
Ověří, že funkce:

- vyvolá očekávanou výjimku,  
- vyvolá správný typ výjimky,  
- vrátí instanci výjimky pro další kontrolu.

---

### 4) **Deep Telemetry Inspection** *(pokud je `deep_check=True`)*
```python
assert_exception_fields(...)
```
Ověří, že výjimka má správné hodnoty:

- `error_name`  
- `label`  
- `message`  
- `expected`  
- `value`  
- `problem`  
- `context`  
- `how_to_fix`  
- `exception`  
- `get_location`  
- `skip_locations`  
- `oneline`

Podporuje:

- substring match (default),  
- exact match,  
- prefix match.

---

## 🎛 Verbosity & Deep Check

### Verbosity
- `verbose=True` → aktivuje subtesty pro všechny kroky.  
- `verbose=False` → pipeline běží bez subtestů.

### Deep Check
- `deep_check=True` → provede všechny kroky včetně kontroly polí.  
- `deep_check=False` → provede jen callable → valid → invalid → typ výjimky.

---

## 📁 Obsah modulu

### `assert_exception_function.py`
Obsahuje orchestrátorovou funkci a design notes.

---

## 🔍 Příklady použití

### Kompletní audit funkce
```python
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_param=("bad",),
    valid_param=("good",),
    message="Something went wrong",
    error_name="MY_ERR",
)
```

### Prefix match
```python
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_param=("bad",),
    message="Invalid",
    startswith=True,
)
```

### Tichý režim
```python
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_param=("bad",),
    verbose=False,
)
```

### Bez hluboké kontroly
```python
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_param=("bad",),
    deep_check=False,
)
```

---

## 🛡️ Architektonické principy

- **Facade Pattern**  
  Orchestrátor sjednocuje tři funkční asserts + field validator.

- **Fail‑Fast**  
  Pokud objekt není callable → pipeline se zastaví.

- **Modularita**  
  Každý krok je samostatný assert.

- **Determinismus**  
  Pipeline má pevně definované pořadí kroků.

- **Fluid API**  
  Funkce vrací instanci výjimky z negativního scénáře.

- **Opt‑in Comparison Modes**  
  substring / exact / prefix.

---
