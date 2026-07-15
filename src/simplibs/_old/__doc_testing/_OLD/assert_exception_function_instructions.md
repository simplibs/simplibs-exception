# `assert_exception_function` — Komplexní audit funkční logiky

`assert_exception_function` je hlavní orchestrátor (vzorec **Facade**) pro testování funkcí a validátorů, které mají vyvolávat výjimky typu `SimpleException` nebo jiné frameworkové chyby.

Provádí kompletní audit v přesně definovaném pořadí:

1. **Ověření volatelnosti** ➔ Je testovaný objekt vůbec funkce?
2. **Čistý průchod (Happy Path)** ➔ Projde funkce s validními daty bez chyby?
3. **Záchyt výjimky** ➔ Vyvolá špatný vstup správný typ výjimky?
4. **Hloubková telemetrie** ➔ Jsou diagnostická pole výjimky kompletní a správná?

---

## 🛠️ Konfigurace a parametry

### Povinné parametry

* **`subtests`** (`Any`) ➔ Instance pytest fixture manažeru pro izolované subtesty.
* **`func`** (`Callable[..., Any]`) ➔ Testovaná funkce nebo validátor.
* **`exception_type`** (`type[BaseException]`) ➔ Očekávaná třída vyvolané výjimky.
* **`invalid_params`** (`tuple | Kwargs`) ➔ Špatná data, která *musí* vyvolat chybu.

### Volitelné parametry

* **`valid_params`** (`tuple | Kwargs`) ➔ Výchozí: `UNSET`. Dobrá data, která nesmí vyvolat žádnou chybu (test pozitivního scénáře).
* **Telemetrická pole** (`error_name`, `label`, `message`, `expected`, `value`, `problem`, `context`, `how_to_fix`, `exception`, `get_location`, `skip_locations`, `oneline`) ➔ Výchozí: `UNSET`. Očekávané hodnoty uvnitř zachycené výjimky.

### Nastavení chování (Přepínače)

* **`exact_match`** (`bool`) ➔ Výchozí: `False`. Vynutí přísnou shodu řetězců pomocí operátoru `==`.
* **`startswith`** (`bool`) ➔ Výchozí: `False`. Ověřuje, zda pole začíná očekávaným textem.
* **`verbose`** (`bool`) ➔ Výchozí: `True`. Rozpadne kontrolu každého pole na samostatný subtest v pytestu.
* **`intro`** (`str`) ➔ Výchozí: `""`. Prefix pro pojmenování testů v konzoli.
* **`deep_check`** (`bool`) ➔ Výchozí: `True`. Pokud je `False`, ověří se pouze typ výjimky a detailní telemetrie polí se přeskočí.

---

## 🧭 Průběh auditní pipeline (4 Fáze)

### Fáze 1: Izolační brána volatelnosti

Framework nejprve ověří, zda předaný objekt splňuje základní kontrakt systému Python a lze jej spustit.

```python
# Interní volání:
assert_function_callable(subtests, func, verbose=verbose, intro=intro)

# Pod kapotou se provádí:
assert callable(func)
```

### Fáze 2: Kontrola čistého průchodu (Happy Path)

Pokud do parametru `valid_params` předáte validní data, orchestrátor je rozbalí a zkusí funkci spustit. Ověřuje se, že stabilní kód neprodukuje náhodné chyby.

```python
# Interní volání:
assert_function_valid_input(subtests, func, valid_params=valid_params, verbose=verbose, intro=intro)

# Pod kapotou se provádí:
args, kwargs = process_params(valid_params)
func(*args, **kwargs)  # Nesmí vyvolat žádnou výjimku
```

### Fáze 3: Záchyt negativního stavu a kontrola typu chyby

Framework spustí funkci s nevalidními daty z `invalid_params` uvnitř bezpečné zóny `pytest.raises`. Pokud funkce nevyvolá chybu, nebo vyvolá úplně jiný typ (např. vestavěný `TypeError` kvůli špatné signatuře), zasáhne vnitřní stráž (**Framework Guard**) a test okamžitě bezpečně ukončí.

```python
# Interní volání:
assert_function_raises(subtests, func, invalid_params=invalid_params, exception_type=exception_type, verbose=verbose, intro=intro)

# Pod kapotou se provádí:
args, kwargs = process_params(invalid_params)

with pytest.raises(BaseException) as exc_info:
    func(*args, **kwargs)

exc = exc_info.value  # Extrahovaná reálná instance výjimky

# Kontrola shody typu výjimky (Framework Guard)
if not isinstance(exc, exception_type):
    pytest.fail("[Framework Guard] Funkce vyvolala neočekávaný typ výjimky!")

assert isinstance(exc, exception_type)
```

### Fáze 4: Hloubkový audit telemetrických polí (Při `deep_check=True`)

V poslední fázi se detailně prozkoumají vnitřnosti zachycené výjimky. Standardně se používá flexibilní vyhledávání podřetězců (`in`), což zabraňuje selhání testů při drobných úpravách formátování textu.

```python
# Interní volání:
assert_exception_fields(subtests, exc, error_name=error_name, label=label, ...)
Výchozí inkluze (lze změnit pomocí exact_match/startswith)

# Pod kapotou se provádí:

if error_name is not UNSET:
    assert error_name in exc.error_name

if label is not UNSET:
    assert label in exc.label

if message is not UNSET:
    assert message in exc.message

if expected is not UNSET:
    assert expected in exc.expected

if value is not UNSET:
    assert value == exc.value

if problem is not UNSET:
    assert problem in exc.problem

if context is not UNSET:
    assert context in exc.context

if how_to_fix is not UNSET:
    assert how_to_fix in exc.how_to_fix

if exception is not UNSET:
    assert exception == exc.exception

if get_location is not UNSET:
    assert get_location == exc.get_location

if skip_locations is not UNSET:
    assert skip_locations == exc.skip_locations

if oneline is not UNSET:
    assert oneline == exc.oneline
```

---

## 🔍 Příklady použití v praxi (Kuchařka)

### Případ 1: Jednoduché testování čistě negativního scénáře

Máme funkci, která striktně chrání systémový blacklist proti přepsání a vyvolává výjimku.

```python
def raise_system_blacklist_mutation_error(value: Any) -> NoReturn:
    """Vyvolá výjimku při pokusu o úpravu read-only systémového blacklistu."""
    raise SimpleExceptionSettingsError(
        value=value,
        label="SimpleExceptionSettings",
        problem="The protected '_SYSTEM_BLACKLIST' attribute is strict read-only metadata.",
        how_to_fix=(
            "Do not attempt to alter the core framework system-level blacklist.",
            "To skip your custom repository paths or wrapper files, append them to: SimpleExceptionSettings.LOCATION_BLACKLIST",
        ),
    )
```

#### Testovací kód:

Ověříme chování jedním přehledným deklarativním blokem:

```python
def test_raise_system_blacklist_mutation_error(subtests):
    """Ověří, že funkce ukončí běh s přesně naplněnou chybovou výjimkou."""
    assert_exception_function(
        subtests,
        raise_system_blacklist_mutation_error,
        invalid_params=("bad-value",),
        exception_type=SimpleExceptionSettingsError,
        value="bad-value",
        label="SimpleExceptionSettings",
        problem="The protected '_SYSTEM_BLACKLIST' attribute is strict read-only metadata.",
        how_to_fix=(
            "Do not attempt to alter the core framework system-level blacklist.",
            "To skip your custom repository paths or wrapper files, append them to: SimpleExceptionSettings.LOCATION_BLACKLIST",
        ),
    )
```

#### Výstup z konzole pro Případ 1:

* **Při `verbose=True` (Detailní trasování vlastností):**

```text
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_callable]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_raises_exception]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_exception_type]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_label]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_value]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_problem]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error SUBPASSED[test_how_to_fix]
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error PASSED
```

* **Při `verbose=False` (Kompaktní produkční výpis):**

```text
test_raise_system_blacklist_mutation_error.py::test_raise_system_blacklist_mutation_error PASSED
```

---

### Případ 2: Parametrizovaný test s kontrolou Happy Path (`valid_params`)

Tato funkce ověřuje interní cache. Přijímá pouze prázdný slovník `{}` (reset stavu), cokoliv jiného musí vyhodit výjimku.

```python
def validate_dynamic_cls_cache(value: Any) -> None:
    """Ověří, že hodnota je prázdný slovník — povoleno pouze pro reset cache."""
    if value != {}:
        raise SimpleExceptionSettingsError(
            value=value,
            label="_dynamic_cls_cache",
            expected="an empty dict {} — for configuration and state reset routines only",
            problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
            how_to_fix=(
                "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
                "To clear this cache manually during hot-reloads or tests, assign an empty dict: SimpleExceptionSettings._dynamic_cls_cache = {}",
            ),
        )
```

#### Testovací kód:

Využijeme sílu `pytest.mark.parametrize` pro otestování celé škály nevalidních typů (string, číslo, nelineární kontejnery) a zároveň do každého průchodu přidáme parametr `valid_params=({},)`, který garantuje, že legitimní reset cache neustále funguje.

```python
@pytest.mark.parametrize("invalid_value", [
    "bad-value",            # String
    123,                    # Číslo
    (),                     # Prázdný tuple
    [],                     # Prázdný list
    {"cached_key": str},    # Neprázdný slovník (pokus o manuální modifikaci)
])
def test_validate_dynamic_cls_cache(subtests, invalid_value):
    """Ověří, že jakýkoliv nevalidní vstup vyvolá ochrannou výjimku a validní projde."""
    assert_exception_function(
        subtests,
        validate_dynamic_cls_cache,
        invalid_params=(invalid_value,),
        valid_params=({},),  # Ověření pozitivního scénáře (Happy Path)
        exception_type=SimpleExceptionSettingsError,
        value=invalid_value,
        label="_dynamic_cls_cache",
        expected="an empty dict {} — for configuration and state reset routines only",
        problem="the multi-inheritance class cache is handled internally and cannot be manually overwritten",
        how_to_fix=(
            "To wipe the framework runtime state safely, invoke: SimpleExceptionSettings.reset()",
            "To clear this cache manually during hot-reloads or tests, assign an empty dict: SimpleExceptionSettings._dynamic_cls_cache = {}",
        ),
    )
```

---

### Případ 3: Izolované testování pozitivních průchodů a oddělený záchyt

Máme složitější validátor, který hlídá, aby blacklist byl striktně složen pouze z `tuple` obsahujícího textové řetězce. Vyhazuje dvě různé chybové zprávy – jednu pro špatný kontejner, druhou pro špatný prvek uvnitř.

```python
def validate_location_blacklist(value: Any) -> None:
    """Ověří, že hodnota je tuple obsahující pouze řetězce."""
    # 1. Kontrola samotného kontejneru
    if not isinstance(value, tuple):
        raise SimpleExceptionSettingsError(
            value=value,
            label="LOCATION_BLACKLIST",
            expected="tuple[str, ...] — a tuple of strings containing filename patterns",
            problem="value is not a tuple",
            how_to_fix=(
                "Wrap the value in a tuple: ('filename.py',)",
                "To set an empty blacklist use an empty tuple: ()",
            ),
        )

    # 2. Kontrola prvků uvnitř kontejneru
    bad_items = [i for i in value if not isinstance(i, str)]
    if bad_items:
        raise SimpleExceptionSettingsError(
            value=bad_items,
            label="LOCATION_BLACKLIST",
            expected="a tuple containing only string elements",
            problem=f"tuple contains invalid non-string elements (found {len(bad_items)} invalid item(s))",
            how_to_fix=(
                "Check all items — each one must be a string (str).",
                "Each item defines a file name pattern that will be skipped during location resolution.",
            ),
        )
```

#### Testovací kód:

Ukázka, jak izolovat pozitivní matici a jak čistě otestovat porušení datového typu na úrovni kontejneru.

```python
# -----------------------------------------------------------------------------
# 1. Matice validních vstupů (Happy Path)
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("valid_input", [
    (),                               # Prázdný tuple
    ("a.py", "b.py"),                 # Naplněný tuple
    ("single_element.py",),           # Jednoprvkový tuple
])
def test_validate_location_blacklist_valid_input(subtests, valid_input):
    """Ověří, že validátor bezpečně propustí prázdné i naplněné textové nuly."""
    assert_function_valid_input(
        subtests,
        validate_location_blacklist,
        valid_params=(valid_input,),  # Bezpečné zabalení do předávaného tuplu
        verbose=False
    )

# -----------------------------------------------------------------------------
# 2. Matice nevalidních vstupů — Chyba typu kontejneru
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("invalid_container", [
    ["a.py", "b.py"],                 # List (špatný typ)
    "a.py",                           # Samotný řetězec
    123,                              # Číslo
    {"a.py", "b.py"},                 # Set
    {"key": "value"},                 # Slovník
])
def test_validate_location_blacklist_invalid_container(subtests, invalid_container):
    """Ověří záchyt špatného datového typu kontejneru na vstupu."""
    assert_exception_function(
        subtests,
        validate_location_blacklist,
        invalid_params=(invalid_container,),
        valid_params=((),),                   # Vzorový čistý stav (prázdný tuple)
        exception_type=SimpleExceptionSettingsError,
        value=invalid_container,
        label="LOCATION_BLACKLIST",
        expected="tuple[str, ...] — a tuple of strings containing filename patterns",
        problem="value is not a tuple",
        how_to_fix=(
            "Wrap the value in a tuple: ('filename.py',)",
            "To set an empty blacklist use an empty tuple: ()",
        ),
    )
```

---
