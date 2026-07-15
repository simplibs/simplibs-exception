# 📦 `assert_exception_function` — Komplexní audit funkční logiky

`assert_exception_function` je hlavní orchestrátor (vzorec **Facade**) testovací infrastruktury pro funkce a validátory v knihovně `SimpleException`. Sjednocuje dílčí kontroly chování kódu na validních i nevalidních vstupech do jedné sekvenční pipeline.

> 💡 **Hledáte podrobný návod a ukázky?** Přejdete na [Uživatelský průvodce s příklady](https://www.google.com/search?q=USER_GUIDE.md).

---

## ⚙️ Architektonické principy

* **Facade Pattern** ➔ Sjednocuje test volatelnosti, pozitivní test, odchycení výjimky a kontrolu jejích polí.
* **Fail‑Fast brána** ➔ Pokud testovaný objekt není funkční (callable), pipeline se okamžitě zastaví.
* **Fluid API** ➔ Funkce vrací zachycenou instanci výjimky z negativního scénáře pro případné doplňkové testy.
* **Opt‑in srovnávání** ➔ Výchozí vyhledávání podřetězců (`in`) lze zpřísnit na přesnou shodu (`exact_match`) nebo prefix (`startswith`).

---

## 🧭 Pipeline kroků

Orchestrátor provádí kroky v tomto přesném pořadí:

1. **Callable Gate** (`assert_function_callable`)
Ověří, zda je testovaný objekt skutečně spustitelný.
2. **Valid Input Sanity Check** (`assert_function_valid_input`)
*Spouští se pouze při zadání `valid_params`.* Ověří, že s dobrými daty funkce projde bez chyb a není permanentně rozbitá.
3. **Negative Boundary Check** (`assert_function_raises`)
Spustí funkci s nevalidními parametry (`invalid_params`), zachytí výjimku a ověří její datový typ. Vrací instanci výjimky.
4. **Deep Telemetry Inspection** (`assert_exception_fields`)
*Spouští se jen při `deep_check=True`.* Detailně zkontroluje všechna nadefinovaná diagnostická pole výjimky.

---

## 🎛️ Přehled konfigurace (Parametry)

### Režimy kontroly (`deep_check`)

* `deep_check=True` ➔ Kompletní audit (všechny 4 kroky včetně hloubkového testu polí).
* `deep_check=False` ➔ Pouze test volatelnosti, happy path a záchyt správného typu výjimky (bez kontroly polí).

### Režimy výpisu (`verbose`)

* `verbose=True` ➔ Aktivuje subtesty pro celou pipeline v pytestu (rozpad na jednotlivá pole).
* `verbose=False` ➔ Vypne subtesty (kompaktní, tichý výstup v konzoli).

---

## 🔍 Rychlé příklady použití

```python
# 1. Kompletní audit (Happy Path, záchyt chyby i kontrola polí)
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_params=("bad-value",),
    valid_params=("good-value",),
    label="MY_LABEL",
    message="Something went wrong",
)

# 2. Rychlá kontrola pouze typu výjimky (rychlý smoke test)
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_params=("bad-value",),
    deep_check=False,
)

# 3. Přísná shoda textových polí (Exact match)
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_params=("bad-value",),
    message="Exact Error Message",
    exact_match=True,
)

# 4. Tichý režim bez pytest subtestů
assert_exception_function(
    subtests,
    my_func,
    exception_type=MyError,
    invalid_params=("bad-value",),
    verbose=False,
)

```