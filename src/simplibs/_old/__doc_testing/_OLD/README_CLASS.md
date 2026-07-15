# 📦 `assert_exception_class` 
**Composite Exception Class Auditor**

`assert_exception_class` je hlavní orchestrátor (vzorec **Facade**) testovací infrastruktury pro výjimky v knihovně `SimpleException`. Sjednocuje čtyři dílčí kontroly do jedné sekvenční pipeline.

## 🧭 Pipeline kroků

Orchestrátor provádí kroky v tomto přesném pořadí:

1. **Inheritance Contract** (`assert_class_inheritance`)  
   Ověří, že výjimka dědí `BaseException` a `SimpleExceptionData`.
2. **Class Defaults Reflection** (`assert_class_defaults`)  
   Ověří výchozí hodnoty instance bez argumentů. Vrací tuto instanci.
3. **Constructor Propagation** (`assert_class_constructor`)  
   *Spouští se jen při `deep_check=True`.* Ověří správné uložení argumentů konstruktoru.
4. **Public API Contract** (`assert_class_interface`)  
   *Spouští se jen při `deep_check=True`.* Ověří přítomnost dunder metod a serializátorů (`to_dict`, `to_json`).



---

## 🧭 Účel modulu

`assert_exception_class` slouží jako:

- **master orchestrátor** pro testování výjimek,  
- **jednotný vstupní bod** pro všechny testy, které validují strukturu výjimky,  
- **automatizovaný kontrolní mechanismus**, který zajišťuje, že výjimka splňuje všechny architektonické požadavky,  
- **základní stavební kámen** pro `bulk_test` a další automatické testovací nástroje.

---

## 🔧 Pipeline kroků

Orchestrátor provádí čtyři kroky v přesně definovaném pořadí:

### 1) **Inheritance Contract**
```python
assert_class_inheritance(...)
```
Ověří, že výjimka dědí:

- `BaseException`,  
- `SimpleExceptionData`.

Pokud selže → pipeline se okamžitě zastaví.

---

### 2) **Class Defaults Reflection**
```python
exc = assert_class_defaults(...)
```
Ověří, že instance bez argumentů má stejné hodnoty jako class-level atributy.

Tento krok zároveň vrací instanci, která je výsledkem orchestrátoru.

---

### 3) **Constructor Propagation** *(jen pokud `deep_check=True`)*
```python
assert_class_constructor(...)
```
Ověří, že konstruktor správně ukládá všechny podporované argumenty.

---

### 4) **Public API Contract** *(jen pokud `deep_check=True`)*
```python
assert_class_interface(...)
```
Ověří, že výjimka implementuje:

- `__str__`,  
- `__repr__`,  
- `to_dict`,  
- `to_debug_dict`,  
- `to_json`.

---

## 🎛 Verbosity & Deep Check

### Verbosity
- `verbose=True` → aktivuje subtesty pro všechny kroky.  
- `verbose=False` → pipeline běží bez subtestů.  
- `verbose_constructor=True` → aktivuje subtesty *jen* pro konstruktor (pokud `verbose=True`).

### Deep Check
- `deep_check=True` → provede všechny kroky.  
- `deep_check=False` → provede jen inheritance + defaults.

---

## 📁 Obsah modulu

### `assert_exception_class.py`
Obsahuje orchestrátorovou funkci a design notes.

---

## 🔍 Příklady použití

### Kompletní audit výjimky
```python
assert_exception_class(subtests, MyError)
```

### Přísnější porovnání defaultů
```python
assert_exception_class(subtests, MyError, exact_match=True)
```

### Prefix match
```python
assert_exception_class(subtests, MyError, startswith=True)
```

### Tichý režim
```python
assert_exception_class(subtests, MyError, verbose=False)
```

### Bez hluboké kontroly
```python
assert_exception_class(subtests, MyError, deep_check=False)
```

---

## 🛡️ Architektonické principy

- **Facade Pattern**  
  Orchestrátor sjednocuje čtyři dílčí asserts do jedné pipeline.

- **Fail‑Fast**  
  Pokud selže dědičnost, nic dalšího se netestuje.

- **Modularita**  
  Každý krok je samostatný assert.

- **Determinismus**  
  Pipeline má pevně definované pořadí kroků.

- **Fluid API**  
  Funkce vrací instanci výjimky z defaultů.

- **Verbosity Hierarchy**  
  Globální verbose + lokální verbose_constructor.

---
