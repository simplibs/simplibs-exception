# 📘 README — *simplibs.exception.testing*

## 🎯 Účel modulu

Modul **simplibs.exception.testing** poskytuje dva specializované testovací helpery určené pro testování výjimek typu **SimpleException**, **SimpleExceptionData**, **SimpleExceptionInternalError**, a všech jejich potomků.

Tyto helpery umožňují:

- testovat funkce, které vyvolávají výjimku,
- testovat přímo třídy výjimek,
- ověřovat všechna diagnostická pole výjimky,
- používat UNSET logiku,
- používat verbose / silent režim,
- používat pytest subtesty pro přehledný výstup.

Modul je navržen tak, aby testování výjimek bylo:

- **jednoduché**  
- **přehledné**  
- **deterministické**  
- **bez boilerplate kódu**  

---

# 📦 Instalace

Modul je součástí knihovny **simplibs.exception**.  
Není potřeba nic dalšího instalovat.

---

# 🧩 Struktura modulu

```
simplibs/exception/testing/
│
├── assert_exception_function.py   # testování funkcí, které výjimku vyvolají
├── assert_exception_class.py      # testování tříd výjimek
│
└── helpers/
    ├── check_exception_fields.py  # společná logika validace polí výjimky
    ├── compare_strings.py         # porovnání textových polí
    ├── manage_param.py            # převod parametru na (args, kwargs)
    └── maybe_subtest.py           # volitelný pytest subtest wrapper
```

---

# 🧪 1) Testování funkcí — `assert_exception_function`

Tento helper je určený pro testování **validačních funkcí**, které po zavolání vyvolají výjimku.

### ✔ Ověří, že funkce výjimku vyvolá  
### ✔ Ověří typ výjimky  
### ✔ Ověří všechna diagnostická pole  
### ✔ Podporuje verbose / silent režim  
### ✔ Podporuje UNSET logiku  

---

## 📌 Ukázka použití

```python
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import SimpleExceptionSettingsError

def validate_dynamic_cls_cache(value):
    if value != {}:
        raise SimpleExceptionSettingsError(
            value=value,
            label="_dynamic_cls_cache",
            expected="an empty dict {} — for configuration and state reset routines only",
            problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
            how_to_fix=(
                "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
                "To clear this cache manually during hot-reloads or tests, assign an empty dict: "
                "SimpleExceptionSettings._dynamic_cls_cache = {}",
            ),
        )

def test_validate_dynamic_cls_cache(subtests):
    assert_exception_function(
        subtests,
        validate_dynamic_cls_cache,
        valid_param={},
        invalid_param="abc",
        exception_type=SimpleExceptionSettingsError,

        error_name="SETTINGS ERROR",
        label="_dynamic_cls_cache",
        expected="an empty dict {} — for configuration and state reset routines only",
        value="abc",
        problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
        how_to_fix=(
            "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
            "To clear this cache manually during hot-reloads or tests, assign an empty dict: "
            "SimpleExceptionSettings._dynamic_cls_cache = {}",
        ),

        verbose=True,
    )
```

---

# 🧪 2) Testování tříd výjimek — `assert_exception_class`

Tento helper je určený pro testování **samotných tříd výjimek**, bez nutnosti volat funkci.

### ✔ Ověří konstrukci výjimky  
### ✔ Ověří všechna diagnostická pole  
### ✔ Ideální pro interní výjimky  
### ✔ Ideální pro testování default hodnot  

---

## 📌 Ukázka použití

```python
from simplibs.exception.testing import assert_exception_class
from simplibs.exception import SimpleExceptionInternalError

def test_internal_error_defaults(subtests):
    assert_exception_class(
        subtests,
        SimpleExceptionInternalError,
        error_name="INTERNAL ERROR",
        oneline=False,
        verbose=True,
    )
```

---

# 🧩 Společná logika — `check_exception_fields`

Oba helpery používají společnou funkci, která ověřuje:

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

Každé pole se ověřuje pouze tehdy, pokud není UNSET.

---

# 🎛 Parametry helperů

### ✔ `valid_param`  
Parametr, který se předá funkci v „validním“ režimu.

### ✔ `invalid_param`  
Parametr, který musí vyvolat výjimku.

### ✔ `exception_type`  
Typ očekávané výjimky.

### ✔ `verbose`  
- `True` → pytest subtesty  
- `False` → tichý režim  

### ✔ `exact_match`  
- `True` → přesná shoda  
- `False` → substring match  

---
