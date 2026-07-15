# 📦 `testing/asserts/functions` 
**Functional Validation Assertion Suite**

Balíček `asserts/functions` obsahuje tři klíčové validační nástroje určené pro testování **funkcí**, které mohou:

- přijímat různé typy parametrů,  
- vyvolávat výjimky,  
- nebo naopak úspěšně zpracovávat validní vstupy.

Tyto asserts tvoří základní stavební kameny vyšších testovacích orchestrátorů:

- `assert_exception_function`  
- `bulk_test`  
- a všech testů, které ověřují funkční logiku výjimek.

---

## 📁 Obsah balíčku

### `assert_function_callable.py`
Validuje, že objekt je skutečně callable.

Než se začne testovat funkční chování, je nutné ověřit, že objekt:

- je funkce,  
- nebo má `__call__`, nebo je jinak invokovatelný.

Tento assert:

- chrání před chybami typu „object is not callable“,  
- poskytuje fail‑fast chování,  
- zajišťuje čisté diagnostické výpisy.

---

### `assert_function_raises.py`
Validuje negativní scénáře — funkce musí vyvolat výjimku.

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
- vše díky `process_params`.

---

### `assert_function_valid_input.py`
Validuje pozitivní scénáře — funkce nesmí vyvolat výjimku.

Tento assert ověřuje:

- že funkce **nevyvolá žádnou výjimku**,  
- že validní vstup je skutečně validní,  
- že funkce není „permanentně rozbitá“,  
- že lze bezpečně pokračovat na negativní testy.

Opět využívá `process_params` pro jednotné zpracování parametrů.

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
    invalid_params=("bad",),
    exception_type=ValueError,
)
```

### Validace, že funkce úspěšně zpracuje validní vstup
```python
assert_function_valid_input(
    subtests,
    my_func,
    valid_params=("good",),
)
```

### Použití s `Kwargs`
```python
from simplibs.exception.testing.tools import Kwargs

assert_function_valid_input(
    subtests,
    my_func,
    valid_params=Kwargs(mode="safe"),
)
```
--