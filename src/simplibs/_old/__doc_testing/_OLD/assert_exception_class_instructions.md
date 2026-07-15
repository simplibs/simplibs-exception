# `assert_exception_class` — Návod k použití

`assert_exception_class` je hlavní orchestrátor celé testovací infrastruktury pro výjimky v knihovně `SimpleException`. Slouží jako jednotný vstupní bod (vzorec **Facade Pattern**), který jedním voláním provede kompletní sérii testů rozdělenou do 4 navazujících kroků:

1. **Dědičnost** (`assert_class_inheritance`)
2. **Výchozí hodnoty** (`assert_class_defaults`)
3. **Konstruktor** (`assert_class_constructor`)
4. **Veřejné API** (`assert_class_interface`)

---

## 🛠️ Konfigurace a parametry

Níže naleznete přehled parametrů, kterými lze chování tohoto orchestrátoru detailně řídit.

### Povinné parametry

* **`subtests`** (`Any`) ➔ Instance pytest fixture manažeru pro izolované subtesty.
* **`exc_class`** (`type[Any]`) ➔ Konkrétní třída výjimky, kterou chceme validovat.

### Volitelné parametry

* **`expected_parents`** (`type[Any] | tuple[type[Any], ...]`) ➔ Výchozí: `UNSET`. Třída nebo tuple tříd, které musí testovaná výjimka povinně dědit (pro ověření polymorfismu).
* **`exact_match`** (`bool`) ➔ Výchozí: `False`. Pokud je `True`, textová pole se porovnávají na absolutní shodu.
* **`startswith`** (`bool`) ➔ Výchozí: `False`. Pokud je `True`, ověřuje, zda pole začíná očekávaným textem.
* **`verbose`** (`bool`) ➔ Výchozí: `True`. Hlavní přepínač, který zapíná detailní rozpad subtestů v pytestu.
* **`verbose_constructor`** (`bool`) ➔ Výchozí: `False`. Pokud je `True`, detailně rozepíše kontrolu každého jednotlivého pole v konstruktoru.
* **`intro`** (`str`) ➔ Výchozí: `""`. Volitelný prefix pro pojmenování generovaných subtestů.
* **`deep_check`** (`bool`) ➔ Výchozí: `True`. Pokud je `True`, spustí pokročilé testy propagace konstruktoru a celého serializačního API.

### Návratová hodnota

* Vrací instanci vytvořené výjimky zachycenou během ověřování výchozích hodnot.

---

## 🧭 Průběh auditní pipeline (4 Fáze)

### Fáze 1: Kontrola hierarchie dědičnosti (Fail-Fast brána)

Tento krok ověřuje, zda testovaná třída správně dědí od základních kamenů systému Pythonu i samotné knihovny. Pokud tato fáze selže, test se okamžitě zastaví, protože nemá smysl testovat parametry na nevalidním objektu.

```python
# Interní volání:
assert_class_inheritance(
    subtests,
    exc_class,
    expected_parents=expected_parents,
    verbose=verbose,
    intro=intro
)

# Pod kapotou se provádí:
assert issubclass(exc_class, BaseException)
assert issubclass(exc_class, SimpleExceptionData)
assert issubclass(exc_class, expected_parents)  # Pouze pokud je zadán očekávaný rodič
```

### Fáze 2: Kontrola výchozích (třídních) hodnot

V této fázi framework vytvoří čistou instanci výjimky bez zadání parametrů a zkontroluje, zda její výchozí stavy odpovídají tomu, co má třída pevně nadefinováno ve svých atributech. K porovnání polí se používá vnitřní funkce `assert_exception_fields`.

```python
# Interní volání:
exc = assert_class_defaults(
    subtests,
    exc_class,
    exact_match=exact_match,
    startswith=startswith,
    verbose=verbose,
    intro=intro
)

# Pod kapotou se provádí extrakce a kontrola polí:
class_dict = exc_class.__dict__
return assert_exception_fields(
    subtests,
    exc,
    error_name=class_dict.get("error_name", UNSET),
    label=class_dict.get("label", UNSET),
    message=class_dict.get("message", UNSET),
    expected=class_dict.get("expected", UNSET),
    value=class_dict.get("value", UNSET),
    problem=class_dict.get("problem", UNSET),
    context=class_dict.get("context", UNSET),
    how_to_fix=class_dict.get("how_to_fix", UNSET),
    exception=class_dict.get("exception", UNSET),
    get_location=class_dict.get("get_location", UNSET),
    skip_locations=class_dict.get("skip_locations", UNSET),
    oneline=class_dict.get("oneline", UNSET),
    exact_match=exact_match,
    startswith=startswith,
    verbose=verbose,
    intro=intro + subintro,
)
```

### Fáze 3: Kontrola propagace konstruktoru (Spouští se při `deep_check=True`)

Framework nasimuluje kompletní předání testovacích dat do všech parametrů konstruktoru najednou. Následně ověří, zda se tato data správně usadila v instanci a zda klíčové identifikátory (jako název chyby a zpráva) správně pronikly do textové reprezentace `str(exc)`.

```python
# Interní volání:
assert_class_constructor(
    subtests,
    exc_class,
    verbose=verbose and verbose_constructor,
    intro=intro
)

# Pod kapotou se provádí:
_message = "<message>"
_value = "<value>"
_label = "<label>"
_expected = "<expected>"
_problem = "<problem>"
_context = "<context>"
_how_to_fix = "<how_to_fix>"
_error_name = "<ERROR_NAME>"
_exception = ValueError("test exception")
_get_location = False
_skip_locations = ("<skip_locations>",)
_oneline = True

# Inicializace testovacího objektu se všemi daty
dummy_exc = exc_class(
    message=_message,
    value=_value,
    label=_label,
    expected=_expected,
    problem=_problem,
    context=_context,
    how_to_fix=_how_to_fix,
    error_name=_error_name,
    exception=_exception,
    get_location=_get_location,
    skip_locations=_skip_locations,
    oneline=_oneline,
)

# 1. Ověření, že instance v sobě drží přesně to, co do ní přišlo
assert_exception_fields(
    subtests, dummy_exc,
    message=_message, value=_value, label=_label, expected=_expected,
    problem=_problem, context=_context, how_to_fix=_how_to_fix,
    error_name=_error_name, exception=_exception, get_location=_get_location,
    skip_locations=_skip_locations, oneline=_oneline,
    exact_match=True, verbose=verbose, intro=intro + subintro,
)

# 2. Kontrola přítomnosti klíčových slov v textovém výstupu výjimky
exc_str = str(dummy_exc)
assert _error_name in exc_str
assert _message in exc_str
```

### Fáze 4: Kontrola veřejného API a serializátorů (Spouští se při `deep_check=True`)

Poslední fáze garantuje datovou integritu výjimky. Ověřuje, že standardní dunder metody vracejí správné datové typy a že všechny vestavěné exportní exportéry (`to_dict`, `to_json`, atd.) fungují bez chyb a generují správné struktury.

```python
# Interní volání:
assert_class_interface(
    subtests,
    exc_class,
    verbose=verbose,
    intro=intro
)

# Pod kapotou se provádí:
assert isinstance(str(exc), str)
assert isinstance(repr(exc), str)
assert isinstance(exc.to_dict(), dict)
assert isinstance(exc.to_debug_dict(), dict)
assert isinstance(exc.to_json(), str)
```

---

## 📖 Příklady použití v praxi

Následující příklad ukazuje, jak otestovat interní knihovní výjimku. Tento scénář demonstruje, že naše testovací nástroje skvěle fungují i na odlehčené objekty postavené na kombinaci `SimpleExceptionData` a `Exception`.

### Použitá testovaná výjimka:

```python
@dataclass
class SimpleExceptionInternalError(SimpleExceptionData, Exception):
    """Interní knihovní výjimka — bez validace, přímý výstup."""

    # Přepsání základního identifikátoru
    error_name: str = "INTERNAL ERROR"

    def __post_init__(self):
        from ...modes import PRETTY
        rendered_message = PRETTY.render(self, validate=False)
        Exception.__init__(self, rendered_message)
```

### Napsané testy:

Ukázka ukazuje, jak `assert_exception_class` odbaví kompletní standardní testování, přičemž vývojáři nic nebrání dopsat si pod to libovolné vlastní specifické aserce (např. kontrolu chování grafického módu).

```python
import pytest

def test_internal_error_basic_contract(subtests):
    """Spustí univerzální sadu testů pro dědičnost, defaulty, konstruktor a rozhraní."""
    assert_exception_class(
        subtests,
        SimpleExceptionInternalError,
        verbose=False
    )

def test_str_contains_rendered_pretty_message():
    """Doplňkový test: Ověření, že PRETTY vykreslení obsahuje kritická data."""
    err = SimpleExceptionInternalError(label="my-label", problem="something broke")
    text = str(err)
    assert "INTERNAL ERROR" in text
    assert "my-label" in text
    assert "something broke" in text

def test_skips_validation_and_never_crashes_on_bad_types():
    """Doplňkový test: Ověření, že interní chyba ignoruje špatné typy a nespadne."""
    err = SimpleExceptionInternalError(label=12345)  # type: ignore
    assert "12345" in str(err)
```

---

## 📊 Porovnání výstupu v terminálu (`verbose`)

Parametr `verbose` mění způsob, jakým pytest zobrazuje výsledky v konzoli. Umožňuje přepínat mezi maximálním detailem a čistým kompaktním pohledem.

### Stav `verbose=True` (Detailní rozpad na subtesty)

Vhodné při ladění nové výjimky – přesně vidíte, která vnitřní kontrola selhala.

```text
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_inheritance::test_base_exception_inheritance]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_inheritance::test_simple_exception_data_inheritance]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_defaults::test_error_name]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_str]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_repr]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_to_dict]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_to_debug_dict]
tests/test_internal_error.py::test_internal_error_basic_contract SUBPASSED[test_class_interface::test_to_json]
tests/test_internal_error.py::test_internal_error_basic_contract PASSED
tests/test_internal_error.py::test_str_contains_rendered_pretty_message PASSED
tests/test_internal_error.py::test_skips_validation_and_never_crashes_on_bad_types PASSED
```

### Stav `verbose=False` (Kompaktní produkční pohled)

Vhodné pro běžné spouštění celé testovací sady – udržuje konzoli čistou a přehlednou.

```text
tests/test_internal_error.py::test_internal_error_basic_contract PASSED
tests/test_internal_error.py::test_str_contains_rendered_pretty_message PASSED
tests/test_internal_error.py::test_skips_validation_and_never_crashes_on_bad_types PASSED
```

---
