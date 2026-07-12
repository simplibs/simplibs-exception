# 📦 `testing/asserts/functions` — Functional Validation Assertion Suite

Balíček `asserts/functions` obsahuje tři klíčové validační nástroje určené pro testování **funkcí**, které mohou:

- přijímat různé typy parametrů,  
- vyvolávat výjimky,  
- nebo naopak úspěšně zpracovávat validní vstupy.

Tyto asserts tvoří základní stavební kameny vyšších testovacích orchestrátorů:

- `assert_exception_function`  
- `bulk_test`  
- a všech testů, které ověřují funkční logiku výjimek.

---

## 🧭 Co tento balíček řeší?

### 1) Validaci, že objekt je skutečně callable (`assert_function_callable`)
Než se začne testovat funkční chování, je nutné ověřit, že objekt:

- je funkce,  
- nebo má `__call__`,  
- nebo je jinak invokovatelný.

Tento assert:

- chrání před chybami typu „object is not callable“,  
- poskytuje fail‑fast chování,  
- zajišťuje čisté diagnostické výpisy.

---

### 2) Validaci, že funkce vyvolá očekávanou výjimku (`assert_function_raises`)
Tento assert ověřuje:

- že funkce vyvolá výjimku při invalidním vstupu,  
- že typ výjimky odpovídá očekávání (pokud je zadán),  
- že výjimka je zachycena bezpečně přes `pytest.raises`,  
- že vývojář může následně zkoumat obsah výjimky (fluid API).

Podporuje:

- scalars,  
- tuple/list,  
- trailing `Kwargs`,  
- raw dict (jako positional payload),  
- vše díky `manage_param`.

---

### 3) Validaci, že funkce úspěšně zpracuje validní vstup (`assert_function_valid_input`)
Tento assert ověřuje:

- že funkce **nevyvolá žádnou výjimku**,  
- že validní vstup je skutečně validní,  
- že funkce není „permanentně rozbitá“,  
- že lze bezpečně pokračovat na negativní testy.

Opět využívá `manage_param` pro jednotné zpracování parametrů.

---

## 🧰 `_utils/manage_param` — Parametrický normalizační engine

Tento modul obsahuje jedinou, ale zásadní funkci:

### `manage_param(param)`
Normalizuje libovolný vstup do:

```python
(args: tuple, kwargs: dict)
```

Podporuje:

- `Kwargs` → čisté kwargs  
- tuple/list → args  
- tuple/list + trailing Kwargs → args + kwargs  
- prázdné sekvence → `(param,)`  
- scalars → `(param,)`  
- dict → `(param,)`  

Tím zajišťuje, že všechny funkční asserts mohou pracovat s jednotným API.

---

## 📁 Obsah balíčku

### `assert_function_callable.py`
Validuje, že objekt je skutečně callable.

### `assert_function_raises.py`
Validuje negativní scénáře — funkce musí vyvolat výjimku.

### `assert_function_valid_input.py`
Validuje pozitivní scénáře — funkce nesmí vyvolat výjimku.

### `_utils/manage_param.py`
Normalizuje parametry do `(args, kwargs)`.

### `__init__.py`
Re-exporty pro čisté API.

---

## 🔍 Příklady použití

### Validace, že funkce je callable
```python
assert_function_callable(subtests, my_func)
```

### Validace, že funkce vyvolá výjimku
```python
assert_function_raises(
    subtests,
    my_func,
    invalid_param=("bad",),
    exception_type=ValueError,
)
```

### Validace, že funkce úspěšně zpracuje validní vstup
```python
assert_function_valid_input(
    subtests,
    my_func,
    valid_param=("good",),
)
```

### Použití s `Kwargs`
```python
from simplibs.exception.testing.tools import Kwargs

assert_function_valid_input(
    subtests,
    my_func,
    valid_param=Kwargs(mode="safe"),
)
```

---

## 🛡️ Architektonické principy

- **Fail‑Fast**  
  Pokud objekt není callable → pipeline se zastaví.

- **Deterministická normalizace parametrů**  
  `manage_param` zajišťuje jednotné chování.

- **Oddělení pozitivních a negativních scénářů**  
  Každý assert řeší jednu oblast.

- **Fluid API**  
  `assert_function_raises` vrací instanci výjimky.

- **Modularita**  
  Každý assert je samostatný, orchestrátor je skládá dohromady.

---
