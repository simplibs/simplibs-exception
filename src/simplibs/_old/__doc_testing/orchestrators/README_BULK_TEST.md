# 📦 `exception_bulk_test` 
***Automatizované maticové testování subsystémů**

Balíček `bulk_test` poskytuje nejvyšší vrstvu testovacího frameworku `SimpleException`. 
Tento automatizovaný orchestrátor umožňuje psát **jediný test**, který kompletně pokryje celou architekturu (třídy výjimek, testovací funkce i komplexní scénáře).

> 💡 Obsah:
> - [⚙️ Architektonické principy](#%EF%B8%8F-architektonické-principy)
> - [🧭 Formáty testovacích položek (Co lze vložit do matice)](#%EF%B8%8F-formáty-testovacích-položek-co-lze-vložit-do-matice)
> - [🔍 Rychlá ukázka matice](#-rychlá-ukázka-matice)
> - [🛠️ Konfigurace a parametry](#%EF%B8%8F-konfigurace-a-parametry)
> - [🧪 Vnitřní mechanika směrování (Jak to funguje pod kapotou)](#-vnitřní-mechanika-směrování-jak-to-funguje-pod-kapotou)
> - [📖 Praktický příklad: Testování celého subsystému nastavení](#-praktický-příklad-testování-celého-subsystému-nastavení)
> - [📊 Vizuální podoba výstupu v terminálu](#-vizuální-podoba-výstupu-v-terminálu)


---

## ⚙️ Architektonické principy
- **Automatické směrování (Routing)** ➔ Engine sám podle signatury pozná typ položky a pošle ji do správného specifického auditoru.
- **Odstranění duplicit** ➔ Umožňuje testovat celé subsystémy formou jednoduchého, přehledného seznamu položek (`ITEMS`).
- **Režimy kontroly (Shallow vs. Deep)** ➔ Možnost přepínat mezi rychlým kouřovým testem (vhodné pro rychlé CI běhy) a hlubokým auditem.


---

## 🧭 Formáty testovacích položek (Co lze vložit do matice)

Orchestrátor `exceptions_bulk_test` automaticky rozpoznává a zpracovává 3 formáty:

1. **Třída výjimky** (`SimpleExceptionInternalError`)  
   Naked třída. Směruje se do `assert_exception_class`. Provádí audit dědičnosti, defaultů a rozhraní.
2. **Inline funkční test** (`tuple(TypVýjimky, Funkce, *Parametry)`)  
   Kompaktní zápis pro rychlé otestování selhání funkce. Směruje se do `assert_exception_function` s vypnutou kontrolou polí.
3. **Komplexní scénář** (`FuncCase`)  
   Deklarativní datový kontejner. Umožňuje hloubkový audit všech telemetrických a diagnostických polí vyvolané výjimky.


---

## 🔍 Rychlá ukázka matice

```python
exceptions_bulk_test(
    subtests,
    items=[
        MyException,                                # 1. Audit třídy
        (MyException, validate_input, "bad_input"), # 2. Inline test funkce
        FuncCase(                                   # 3. Komplexní scénář
            func=validate_input,
            invalid_params=("bad_input",),
            exception_type=MyException,
            message="Očekávaná zpráva",
        )
    ],
    deep_check=False
)
```

[🔼 Zpět na obsah](#-obsah)

---

## 🛠️ Konfigurace a parametry

Níže naleznete přehled parametrů, kterými lze chování tohoto orchestrátoru detailně řídit.

### Povinné parametry

* **`subtests`** (`Any`) ➔ Instance pytest fixture manažeru pro izolované subtesty.
* **`items`** (`list[Any]`) ➔ A heterogeneous collection of validation targets.

### Volitelné parametry

* **`exact_match`** (`bool`) ➔ Výchozí: `False`. Pokud je `True`, textová pole se porovnávají na absolutní shodu.
* **`startswith`** (`bool`) ➔ Výchozí: `False`. Pokud je `True`, ověřuje, zda pole začíná očekávaným textem.
* **`verbose`** (`bool`) ➔ Výchozí: `True`. Hlavní přepínač, který zapíná detailní rozpad subtestů v pytestu.
* **`deep_check`** (`bool`) ➔ Výchozí: `True`. Pokud je `True`, spustí pokročilé testy propagace konstruktoru a celého serializačního API.

### Raises:
* **`AssertionError`** ➔ If an item fails to match any supported format signatures.

### Návratová hodnota

* **`None`** ➔ Funkce nevrací žádnou hodnotu.

```python
# Ukázka hlavičky funkce:
def exceptions_bulk_test(
    subtests: Any,
    items: list[Any],
    *,
    exact_match: bool = False,
    startswith: bool = False,
    verbose: bool = True,
    deep_check: bool = False,
) -> None:
```

[🔼 Zpět na obsah](#-obsah)

---

## 🧪 Vnitřní mechanika směrování (Jak to funguje pod kapotou)

Když předáte seznam položek do funkce `exceptions_bulk_test`, orchestrátor prochází prvek po prvku a provádí automatický routing:

```python
for item in items:
    # 1. Zpracování komplexních scénářů FuncCase
    if isinstance(item, FuncCase):
        item.run_test(
            subtests,
            exact_match=exact_match,
            startswith=startswith,
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )

    # 2. Zpracování samotných tříd výjimek (Strukturální audit blueprintu)
    elif is_exception_class(item):
        exc_class = item
        assert_exception_class(
            subtests,
            exc_class,
            exact_match=exact_match,
            startswith=startswith,
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )

    # 3. Zpracování inline parametrických sekvencí (Rychlé testy funkcí)
    elif is_exception_function(item):
        # Rozbalení tuplu: (TypVýjimky, Funkce, *Parametry)
        exc_class, func, raw_params = item[0], item[1], item[2:]
        assert_exception_function(
            subtests,
            func,
            invalid_params=raw_params,
            exception_type=exc_class,
            exact_match=exact_match,
            startswith=startswith,
            verbose=verbose,
            intro=intro,
            deep_check=False,
        )
        
     # 4. Fallback gate throwing strict alerts on invalid format tokens
    else:
        with maybe_subtest(subtests, name="unknown_item", verbose=verbose):
            raise AssertionError(f"Unsupported item signature footprint: {item!r}")           
            
```

[🔼 Zpět na obsah](#-obsah)

---

## 📖 Praktický příklad: Testování celého subsystému nastavení

Následující reálná ukázka demonstruje, jak lze pomocí jedné testovací matice kompletně otestovat 3 třídy výjimek, 1 komplexní scénář s hloubkovou kontrolou polí a 7 standardních validačních funkcí najednou.

### Testovací matice a kód testu:

```python
import pytest
from simplibs.exception._core_logic.internal_exceptions import (
    SimpleExceptionInternalError, SimpleExceptionModeError, SimpleExceptionSettingsError
)
from simplibs.exception._core_logic.settings_meta.validations import (
    raise_unknown_settings_attribute_error, raise_system_blacklist_mutation_error,
    validate_dynamic_cls_cache, validate_get_location, validate_location_blacklist,
    validate_message_mode, validate_value_truncation_length
)

# Pomocná třída pro simulaci vstupu
class DummyClass:
    _VALIDATORS = {"GET_LOCATION": validate_get_location}

# 1. Definice komplexního scénáře pro cache validátor
VALIDATE_DYNAMIC_CLS_CACHE_CASE = FuncCase(
    func=validate_dynamic_cls_cache,
    valid_params={},
    invalid_params="abc",
    exception_type=SimpleExceptionSettingsError,
    error_name="SETTINGS ERROR",
    label="_dynamic_cls_cache",
    expected="an empty dict {} — for configuration and state reset routines only",
    value="abc",
    problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
    how_to_fix=(
        "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
        "To clear this cache manually during hot-reloads or tests, assign an empty dict: SimpleExceptionSettings._dynamic_cls_cache = {}",
    )
)

# 2. Sestavení ucelené matice komponent subsystému
ITEMS = [
    # A) Definice tříd výjimek (Strukturální kontrola)
    SimpleExceptionInternalError,
    SimpleExceptionModeError,
    SimpleExceptionSettingsError,

    # B) Komplexní scénář s detailním auditem polí
    VALIDATE_DYNAMIC_CLS_CACHE_CASE,

    # C) Inline testy funkcí generujících výjimky (bez parametrů / s parametry)
    (SimpleExceptionSettingsError, raise_unknown_settings_attribute_error, DummyClass, "name"),
    (SimpleExceptionSettingsError, raise_system_blacklist_mutation_error, "value"),
    (SimpleExceptionSettingsError, validate_dynamic_cls_cache, "invalid_input"),
    (SimpleExceptionSettingsError, validate_get_location, "invalid_input"),
    (SimpleExceptionSettingsError, validate_location_blacklist, "invalid_input"),
    (SimpleExceptionSettingsError, validate_location_blacklist, (1,)),
    (SimpleExceptionSettingsError, validate_message_mode, "invalid_input"),
    (SimpleExceptionSettingsError, validate_value_truncation_length, "invalid_input"),
    (SimpleExceptionSettingsError, validate_value_truncation_length, -1),
]

def test_settings_subsystem_bulk(subtests):
    """Jeden master test pokrývající kompletní sadu prvků nastavení."""
    exceptions_bulk_test(
        subtests, 
        ITEMS, 
        verbose=True, 
        deep_check=False  # Nastaveno na False pro rychlý kouřový CI test
    )
```

[🔼 Zpět na obsah](#-obsah)

---

## 📊 Vizuální podoba výstupu v terminálu

Když spustíte test subsystému s parametrem `verbose=True`, pytest díky vestavěným subtestům vytvoří nádherně strukturovaný strom reportů. Každá položka dostane svůj automatický prefix podle názvu třídy nebo funkce.

```text
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_SimpleExceptionInternalError::test_class_inheritance::test_base_exception_inheritance]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_SimpleExceptionInternalError::test_class_defaults::test_error_name]
...
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_callable]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_raises_exception]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_label]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_problem]
...
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_raise_unknown_settings_attribute_error::test_callable]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_raise_unknown_settings_attribute_error::test_raises_exception]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_value_truncation_length::test_raises_exception]
test_bulk.py::test_settings_subsystem_bulk PASSED
```

Pokud přepnete na `verbose=False`, celý tento masivní audit subsystému se v konzoli smrskne do jediného, čistého řádku:

```text
test_bulk.py::test_settings_subsystem_bulk PASSED
```

[🔼 Zpět na obsah](#-obsah)

---