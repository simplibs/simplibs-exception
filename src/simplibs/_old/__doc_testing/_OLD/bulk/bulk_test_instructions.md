# Uživatelský průvodce pro `bulk_test` (Maticové testování)

Psaní samostatných testů pro každou výjimku a každou validační funkci vede k obrovskému množství duplicitního kódu. Balíček `bulk_test` tento problém řeší. Umožňuje vám vytvořit jeden přehledný seznam (matici), do kterého poskládáte komponenty celého subsystému, a orchestrátor je sám odbaví.

---

## 🧩 Stavební kámen: `FuncCase`

Pokud potřebujete u nějaké funkce otestovat nejen to, že vyvolá chybu, ale chcete detailně zkontrolovat její vnitřní diagnostická data (`label`, `problem`, `how_to_fix`), použijte deklarativní kontejner `FuncCase`.

```python
# Konstruktor třídy FuncCase přijímá kompletní specifikaci očekávání:
case = FuncCase(
    func=validate_dynamic_cls_cache,       # Testovaná funkce
    invalid_params=("abc",),               # Špatný vstup vyvolávající chybu
    valid_params=({},),                    # Volitelný dobrý vstup (Happy Path)
    exception_type=SimpleExceptionSettingsError, # Očekávaný typ výjimky

    # Očekávaná diagnostická data uvnitř výjimky:
    error_name="SETTINGS ERROR",
    label="_dynamic_cls_cache",
    expected="an empty dict {} — for configuration and state reset routines only",
    value="abc",
    problem="the multi-inheritance class cache is handled internally...",
    how_to_fix=("To wipe the framework runtime state safely...",)
)
```

---

## 🧭 Vnitřní mechanika směrování (Jak to funguje pod kapotou)

Když předáte seznam položek do funkce `exceptions_bulk_test`, orchestrátor prochází prvek po prvku a provádí automatický routing:

```python
for item in items:
    # 1. Zpracování komplexních scénářů FuncCase
    if isinstance(item, FuncCase):
        item.run_test(subtests, deep_check=deep_check, ...)

    # 2. Zpracování samotných tříd výjimek (Strukturální audit blueprintu)
    elif is_exception_class(item):
        assert_exception_class(subtests, exc_class=item, deep_check=deep_check, ...)

    # 3. Zpracování inline parametrických sekvencí (Rychlé testy funkcí)
    elif is_exception_function(item):
        # Rozbalení tuplu: (TypVýjimky, Funkce, *Parametry)
        exc_class, func, raw_params = item[0], item[1], item[2:]
        assert_exception_function(subtests, func, invalid_params=raw_params, exception_type=exc_class, deep_check=False, ...)
```

---

## 🔍 Praktický příklad: Testování celého subsystému nastavení

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

---

## 📊 Vizuální podoba výstupu v terminálu

Když spustíte test subsystému s parametrem `verbose=True`, pytest díky vestavěným subtestům vytvoří nádherně strukturovaný strom reportů. Každá položka dostane svůj automatický prefix podle názvu třídy nebo funkce.

```text
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_SimpleExceptionInternalError::test_class_inheritance::test_base_exception_inheritance]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_SimpleExceptionInternalError::test_class_defaults::test_error_name]
... [audity tříd dokončeny] ...
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_callable]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_raises_exception]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_label]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_dynamic_cls_cache::test_problem]
... [audity polí FuncCase dokončeny] ...
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_raise_unknown_settings_attribute_error::test_callable]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_raise_unknown_settings_attribute_error::test_raises_exception]
test_bulk.py::test_settings_subsystem_bulk SUBPASSED[test_validate_value_truncation_length::test_raises_exception]
test_bulk.py::test_settings_subsystem_bulk PASSED
```

Pokud přepnete na `verbose=False`, celý tento masivní audit subsystému se v konzoli smrskne do jediného, čistého řádku:

```text
test_bulk.py::test_settings_subsystem_bulk PASSED
```
