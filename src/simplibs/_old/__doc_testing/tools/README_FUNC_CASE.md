# 📦 `FuncCase` 
**Nástroj pro kompletní audit funkce v bulk testu**

`FuncCase` je specializovaný **deklarativní datový kontejner**, který slouží k popisu jednoho uceleného funkčního testovacího scénáře. Namísto psaní imperativního testovacího kódu (krok za krokem) vám `FuncCase` umožňuje popsat **co** se má otestovat a **jaká** jsou očekávaná diagnostická data vyvolané výjimky.

Kompletně odděluje definici testu od jeho spouštění, což umožňuje scénáře snadno sdílet, organizovat a dynamicky spouštět buď samostatně, nebo uvnitř maticových testů.

> 💡 Obsah:
> - [⚙️ Architektonické principy FuncCase](#%EF%B8%8F-architektonické-principy-funccase)
> - [📦 Konfigurace a parametry](#-konfigurace-a-parametry)
> - [🔍 Ukázka konstrukce třídy](#-ukázka-konstrukce-třídy)
> - [📖 Příklady použití](#-jak-se-funccase-chová-a-definuje)


---

### ⚙️ Architektonické principy `FuncCase`

* **Deklarativní design:** Odstraňuje imperativní kód ("jak" testovat) a nahrazuje ho popisem stavu ("co" se očekává). Testy jsou díky tomu extrémně čitelné a snadno udržovatelné.
* **Typová a rozhraní integrita:** Všechny parametry jsou typované a odpovídají přesně struktuře a polím výjimek rodiny `SimpleException`.
* **Dynamic Decoupling:** Oddělení definice od runtime parametrů (jako je `verbose` nebo `exact_match`). Tyto parametry se konfigurují až při samotném spuštění (`.run_test` nebo v orchestrátoru).

---

## 🛠️ Konfigurace a parametry

### Povinné atributy třídy FuncCase

* **`func`** (`Callable[..., Any]`) ➔ Testovaná funkce nebo validátor.
* **`exception_type`** (`type[BaseException]`) ➔ Očekávaná třída vyvolané výjimky.
* **`invalid_params`** (`tuple | Kwargs`) ➔ Špatná data, která *musí* vyvolat chybu.

### Volitelné atributy třídy FuncCase

* **`valid_params`** (`tuple | Kwargs`) ➔ Výchozí: `UNSET`. Dobrá data, která nesmí vyvolat žádnou chybu (test pozitivního scénáře).
* **Telemetrická pole** (`error_name`, `label`, `message`, `expected`, `value`, `problem`, `context`, `how_to_fix`, `exception`, `get_location`, `skip_locations`, `oneline`) ➔ Výchozí: `UNSET`. Očekávané hodnoty uvnitř zachycené výjimky.

### Povinné parametry pro interní metodu run_test

* **`subtests`** (`Any`) ➔ Instance pytest fixture manažeru pro izolované subtesty.

### Volitelné parametry pro interní metodu run_test

* **`exact_match`** (`bool`) ➔ Výchozí: `False`. Vynutí přísnou shodu řetězců pomocí operátoru `==`.
* **`startswith`** (`bool`) ➔ Výchozí: `False`. Ověřuje, zda pole začíná očekávaným textem.
* **`verbose`** (`bool`) ➔ Výchozí: `True`. Rozpadne kontrolu každého pole na samostatný subtest v pytestu.
* **`intro`** (`str`) ➔ Výchozí: `""`. Prefix pro pojmenování testů v konzoli.
* **`deep_check`** (`bool`) ➔ Výchozí: `True`. Pokud je `False`, ověří se pouze typ výjimky a detailní telemetrie polí se přeskočí.


### Návratová pro interní metodu run_test

* The caught, instantiated exception object.

[🔼 Zpět na obsah](#-obsah)

---

## 🔍 Ukázka konstrukce třídy

```python
@dataclass(slots=True, kw_only=True)
class FuncCase:

    # Povinné atributy
    func: Callable[..., Any]
    exception_type: type[BaseException]
    invalid_params: tuple[Any, ...] | Kwargs
    
    # Volitelné atributy
    valid_params: tuple[Any, ...] | Kwargs | UnsetType = UNSET
    error_name: str | UnsetType = UNSET
    label: str | None | UnsetType = UNSET
    message: str | None | UnsetType = UNSET
    expected: str | None | UnsetType = UNSET
    value: Any = UNSET
    problem: str | tuple[str, ...] | None | UnsetType = UNSET
    context: str | tuple[str, ...] | None | UnsetType = UNSET
    how_to_fix: str | tuple[str, ...] | None | UnsetType = UNSET
    exception: Exception | type[Exception] | None | UnsetType = UNSET
    get_location: bool | int | UnsetType = UNSET
    skip_locations: tuple[str, ...] | UnsetType = UNSET
    oneline: bool | UnsetType = UNSET

    # Metoda pro testování
    def run_test(
        self,
        subtests: Any,
        *,
        exact_match: bool = False,
        startswith: bool = False,
        verbose: bool = True,
        intro: str = "",
        deep_check: bool = True,
    ) -> BaseException:
        return assert_exception_function(
            subtests,
            self.func,
            valid_params=self.valid_params,
            invalid_params=self.invalid_params,
            exception_type=self.exception_type,
            error_name=self.error_name,
            label=self.label,
            message=self.message,
            expected=self.expected,
            value=self.value,
            problem=self.problem,
            context=self.context,
            how_to_fix=self.how_to_fix,
            exception=self.exception,
            get_location=self.get_location,
            skip_locations=self.skip_locations,
            oneline=self.oneline,
            exact_match=exact_match,
            startswith=startswith,
            verbose=verbose,
            intro=intro,
            deep_check=deep_check,
        )
```

[🔼 Zpět na obsah](#-obsah)

---

## 📖 Příklady použití

### Jak se `FuncCase` chová a definuje

Třída `FuncCase` v sobě sdružuje testovanou funkci, parametry (validní i nevalidní) a kompletní sadu očekávaných telemetrických polí výjimky `SimpleException`:

```python
# Definice testovacího případu jako čisté datové struktury
validate_cache_case = FuncCase(
    func=validate_dynamic_cls_cache,             # Testovaná logika
    valid_params={},                             # Happy path parametry (volitelné)
    invalid_params="abc",                        # Vstup, který musí vyvolat chybu
    exception_type=SimpleExceptionSettingsError, # Očekávaný typ výjimky

    # Deklarativní očekávání (audit telemetrie):
    error_name="SETTINGS ERROR",
    label="_dynamic_cls_cache",
    expected="an empty dict {}",
    value="abc",
    problem="the multi-inheritance class cache is handled internally...",
    how_to_fix="To wipe the framework runtime state safely, invoke..."
)
```

### Samostatné spuštění scénáře

Ačkoli je `FuncCase` navržen primárně pro hromadné matice, můžete jej kdykoli spustit i zcela samostatně přímo v pytestu pomocí metody `.run_test()`:

```python
def test_cache_validation_standalone(subtests):
    # Spuštění kompletní pipeline (Callable -> Valid Input -> Exception -> Fields)
    exc_instance = validate_cache_case.run_test(
        subtests,
        verbose=True,      # Rozpadne kontrolu jednotlivých polí na subtesty
        deep_check=True,   # Provede hloubkový audit všech polí
    )
    
    # Metoda run_test vrací zachycenou instanci výjimky pro případné další aserce
    assert exc_instance.custom_dynamic_property is None
```

[🔼 Zpět na obsah](#-obsah)

---