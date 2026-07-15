# 📦 `testing/asserts/classes` — Exception Class Structural Validation Suite

Balíček `asserts/classes` obsahuje čtyři klíčové validační nástroje, které společně tvoří kompletní testovací pipeline pro ověřování **struktury**, **defaultů**, **konstruktoru** a **public API** výjimek v knihovně **SimpleException**.

Tyto asserts jsou základní stavební kameny vyšších testovacích orchestrátorů:

- `assert_exception_class`  
- `assert_exception_function`  
- `bulk_test`  

Každý assert řeší jednu přesně definovanou oblast — dohromady tvoří kompletní auditní sadu pro jakoukoliv výjimku.

---

## 🧭 Co tento balíček řeší?

### 1) Inheritance Contract (`assert_class_inheritance`)
Každá výjimka musí splňovat dvě zásadní podmínky:

- být potomkem `BaseException`,  
- být potomkem `SimpleExceptionData`.

Tento assert zajišťuje:

- fail‑fast chování (pokud chybí BaseException → okamžitě selže),  
- jistotu, že výjimka má správný datový model,  
- jistotu, že výjimka je skutečná Python výjimka.

---

### 2) Default Values Reflection (`assert_class_defaults`)
Každá výjimka má class-level defaulty:

```python
class MyError(SimpleExceptionData, Exception):
    error_name = "MY_ERROR"
    label = "core"
```

Tento assert ověřuje:

- že instance bez argumentů má stejné hodnoty jako class-level atributy,  
- že konstruktor defaulty nemění,  
- že výjimka je deterministická a čistá.

Používá reflexi přes `exc_class.__dict__`, aby testoval **pouze to, co je deklarováno na třídě**.

---

### 3) Constructor Propagation (`assert_class_constructor`)
Každá výjimka musí správně přijímat a ukládat všechny podporované argumenty:

- `message`  
- `value`  
- `label`  
- `expected`  
- `problem`  
- `context`  
- `how_to_fix`  
- `error_name`  
- `exception`  
- `get_location`  
- `skip_locations`  
- `oneline`

Tento assert:

- vytvoří instanci s kompletní sadou argumentů,  
- ověří, že instance obsahuje přesně ty hodnoty, které byly předány,  
- odhalí jakékoliv mutace, ztrátu dat nebo sabotáže v konstruktoru.

---

### 4) Public API Contract (`assert_class_interface`)
Každá výjimka musí implementovat:

- `__str__()`  
- `__repr__()`  
- `to_dict()`  
- `to_debug_dict()`  
- `to_json()`

Tento assert ověřuje:

- že všechny metody existují,  
- že vrací správné typy (string, dict, string),  
- že výjimka je kompatibilní s layout enginem, logováním a serializací.

---

## 📁 Obsah balíčku

### `assert_class_inheritance.py`
Validuje základní typovou hierarchii výjimky.

### `assert_class_defaults.py`
Validuje class-level defaulty a jejich propagaci do instance.

### `assert_class_constructor.py`
Validuje správné mapování všech konstruktorových argumentů.

### `assert_class_interface.py`
Validuje public API výjimky (stringové metody a serializace).

### `__init__.py`
Re-exporty pro čisté API.

---

## 🔍 Příklady použití

### Kompletní audit jedné výjimky
```python
from simplibs.exception.testing.assert_exception_class import assert_exception_class

def test_my_error(subtests):
    assert_exception_class(subtests, MyError)
```

### Samostatná kontrola defaultů
```python
assert_class_defaults(subtests, MyError)
```

### Samostatná kontrola konstruktoru
```python
assert_class_constructor(subtests, MyError)
```

### Samostatná kontrola public API
```python
assert_class_interface(subtests, MyError)
```

### Samostatná kontrola dědičnosti
```python
assert_class_inheritance(subtests, MyError)
```

---

## 🛡️ Architektonické principy

- **Fail‑Fast**  
  Inheritance je kontrolováno jako první — pokud selže, nic dalšího se netestuje.

- **Single Source of Truth**  
  Constructor test používá interní referenční matici hodnot.

- **Reflexe class-level atributů**  
  Defaulty se čtou z `exc_class.__dict__`, ne z instance.

- **Deterministické API**  
  Interface test ověřuje pouze typy, ne obsah.

- **Modularita**  
  Každý assert řeší jednu oblast, orchestrátor je skládá dohromady.

- **Fluid API**  
  Každý assert vrací instanci nebo třídu → snadné řetězení.

---
