# 📦 Nástroj 2: `exceptions_bulk_test` (Maticový orchestrátor)

## Uživatelský průvodce: `exceptions_bulk_test`

`exceptions_bulk_test` je hlavní testovací orchestrátor (implementující vzorec **Facade**) navržený tak, aby minimalizoval duplicitu testovacího kódu. Umožňuje definovat celou testovací matici pro kompletní subsystém jako jeden přehledný seznam (`ITEMS`) a spustit ho v rámci jednoho master testu.

Engine disponuje **automatickým směrováním (routingem)** – podle tvaru a signatury každého prvku sám rozpozná, o jaký typ testu se jedná, a předá ho správnému specializovanému auditoru.

---

### 🧭 Podporované formáty vstupů v matici

Orchestrátor v seznamu `items` automaticky rozpoznává a odbavuje tři typy zápisů:

1. **Naked třída výjimky** (`SimpleExceptionError`)
*Směrováno na:* `assert_exception_class`.
Ověří dědičnost, standardní chování konstruktoru bez parametrů a správnost rozhraní.
2. **Inline funkční test** (Tuple: `(TypVýjimky, Funkce, *Parametry)`)
*Směrováno na:* `assert_exception_function` (v rychlém režimu).
Rychlý způsob, jak otestovat, že konkrétní funkce se špatnými parametry vyvolá správný typ výjimky.
3. **Komplexní scénář** (`FuncCase`)
*Směrováno na:* `.run_test()` instance `FuncCase`.
Hloubkový audit funkční logiky i všech detailních polí výjimky.

---

### 🔍 Praktický příklad: Testování subsystému nastavení

Následující reálný příklad ukazuje, jak jedinou maticí kompletně otestovat definice tříd, rychlé pomocné "raise" funkce i složitější validační logiku s detailním auditem.

```python
import pytest
from simplibs.exception.testing import exceptions_bulk_test, FuncCase
from simplibs.exception._core_logic.internal_exceptions import (
    SimpleExceptionInternalError, SimpleExceptionModeError, SimpleExceptionSettingsError
)
from simplibs.exception._core_logic.settings_meta.validations import (
    raise_unknown_settings_attribute_error, raise_system_blacklist_mutation_error,
    validate_dynamic_cls_cache, validate_get_location, validate_location_blacklist
)

# 1. Definice komplexního scénáře pro cache (FuncCase)
VALIDATE_CACHE_CASE = FuncCase(
    func=validate_dynamic_cls_cache,
    valid_params={},
    invalid_params="abc",
    exception_type=SimpleExceptionSettingsError,
    error_name="SETTINGS ERROR",
    label="_dynamic_cls_cache",
    expected="an empty dict {}",
    value="abc"
)

# 2. Sestavení matice všech prvků subsystému
SETTINGS_SUBSYSTEM_ITEMS = [
    # A) Strukturální audity samotných tříd výjimek
    SimpleExceptionInternalError,
    SimpleExceptionModeError,
    SimpleExceptionSettingsError,

    # B) Komplexní testovací scénář (FuncCase)
    VALIDATE_CACHE_CASE,

    # C) Inline rychlé testy funkcí (Tuple)
    (SimpleExceptionSettingsError, raise_unknown_settings_attribute_error, "dummy_class", "attr_name"),
    (SimpleExceptionSettingsError, raise_system_blacklist_mutation_error, "forbidden_value"),
    (SimpleExceptionSettingsError, validate_get_location, "invalid_input"),
    (SimpleExceptionSettingsError, validate_location_blacklist, (123,)) # Nevalidní typ v blacklistu
]

# 3. Master test spouštějící celou matici najednou
def test_settings_subsystem(subtests):
    exceptions_bulk_test(
        subtests,
        items=SETTINGS_SUBSYSTEM_ITEMS,
        verbose=True,      # Každý prvek a každá aserce vytvoří vlastní pytest subtest
        deep_check=False,  # Shallow režim pro rychlý vývoj / CI běh
    )

```

---

### 🛡️ Architektonické principy `exceptions_bulk_test`

* **Dynamic Footprint Routing:** Sémantický směrovač analyzuje strukturu objektu (zda jde o třídu, tuple nebo instanci `FuncCase`) za běhu. Odpadá nutnost explicitně registrovat typy testů.
* **Oddělení hloubky kontroly (Shallow vs. Deep):** Pomocí flagu `deep_check` lze globálně přepínat úroveň přísnosti pro celou matici najednou (např. vynutit plné testy serializace výjimek).
* **Bezpečný Fallback Gate:** Pokud se v matici objeví nepodporovaná struktura nebo neznámý objekt, orchestrátor okamžitě vyvolá přehledný `AssertionError` s přesným popisem nevalidního prvku, aby se předešlo tichému ignorování neotestovaného kódu.
