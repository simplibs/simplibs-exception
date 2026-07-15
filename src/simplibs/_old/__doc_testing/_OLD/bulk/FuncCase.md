# 📦 Nástroj 1: `FuncCase`
**Nástroj pro kompletní audit funkce v bulk testu**

## Uživatelský průvodce: `FuncCase`

`FuncCase` je specializovaný **deklarativní datový kontejner**, který slouží k popisu jednoho uceleného funkčního testovacího scénáře. Namísto psaní imperativního testovacího kódu (krok za krokem) vám `FuncCase` umožňuje popsat **co** se má otestovat a **jaká** jsou očekávaná diagnostická data vyvolané výjimky.

Kompletně odděluje definici testu od jeho spouštění, což umožňuje scénáře snadno sdílet, organizovat a dynamicky spouštět buď samostatně, nebo uvnitř maticových testů.

---

### 🛠️ Jak se `FuncCase` chová a definuje

Třída `FuncCase` v sobě sdružuje testovanou funkci, parametry (validní i nevalidní) a kompletní sadu očekávaných telemetrických polí výjimky `SimpleException`:

```python
from simplibs.exception.testing.auxiliary_classes import FuncCase
from simplibs.exception._core_logic.settings_meta.validations import validate_dynamic_cls_cache
from simplibs.exception._core_logic.internal_exceptions import SimpleExceptionSettingsError

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

### 🔍 Samostatné spuštění scénáře

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

---

### 🛡️ Architektonické principy `FuncCase`

* **Deklarativní design:** Odstraňuje imperativní kód ("jak" testovat) a nahrazuje ho popisem stavu ("co" se očekává). Testy jsou díky tomu extrémně čitelné a snadno udržovatelné.
* **Typová a rozhraní integrita:** Všechny parametry jsou typované a odpovídají přesně struktuře a polím výjimek rodiny `SimpleException`.
* **Dynamic Decoupling:** Oddělení definice od runtime parametrů (jako je `verbose` nebo `exact_match`). Tyto parametry se konfigurují až při samotném spuštění (`.run_test` nebo v orchestrátoru).

---

---

* 