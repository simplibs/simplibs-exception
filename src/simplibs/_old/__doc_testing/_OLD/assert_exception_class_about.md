# 📦 `assert_exception_class` — Komplexní audit třídy výjimky

`assert_exception_class` je hlavní orchestrátor (vzorec **Facade**) testovací infrastruktury pro výjimky v knihovně `SimpleException`. Sjednocuje čtyři dílčí kontroly do jedné sekvenční pipeline.

> 💡 **Hledáte podrobný návod a ukázky?** Přejděte na [Uživatelský průvodce s příklady](USER_GUIDE.md).

---

## ⚙️ Architektonické principy
- **Facade Pattern** ➔ Jeden vstupní bod pro kompletní audit struktury výjimky.
- **Fail‑Fast brána** ➔ Pokud selže kontrola dědičnosti, pipeline se okamžitě zastaví.
- **Fluid API** ➔ Funkce vrací zachycenou instanci výjimky z testu výchozích hodnot.
- **Hierarchie upovídanosti** ➔ Globální `verbose` řídí subtesty, `verbose_constructor` je jemné ladění.

---

## 🧭 Pipeline kroků

Orchestrátor provádí kroky v tomto přesném pořadí:

1. **Inheritance Contract** (`assert_class_inheritance`)  
   Ověří, že výjimka dědí `BaseException` a `SimpleExceptionData`.
2. **Class Defaults Reflection** (`assert_class_defaults`)  
   Ověří výchozí hodnoty instance bez argumentů. Vrací tuto instanci.
3. **Constructor Propagation** (`assert_class_constructor`)  
   *Spouští se jen při `deep_check=True`.* Ověří správné uložení argumentů konstruktoru.
4. **Public API Contract** (`assert_class_interface`)  
   *Spouští se jen při `deep_check=True`.* Ověří přítomnost dunder metod a serializátorů (`to_dict`, `to_json`).

---

## 🎛️ Přehled konfigurace (Parametry)

### Režimy kontroly (`deep_check`)
- `deep_check=True` ➔ Kompletní audit (všechny 4 kroky).
- `deep_check=False` ➔ Pouze dědičnost + výchozí hodnoty.

### Režimy výpisu (`verbose`)
- `verbose=True` ➔ Aktivuje subtesty pro celou pipeline.
- `verbose=False` ➔ Vypne subtesty (čistý kompaktní výstup).
- `verbose_constructor=True` ➔ Aktivuje subtesty *specificky* pro konstruktor (vyžaduje `verbose=True`).

---

## 🔍 Rychlé příklady použití

```python
# 1. Standardní kompletní audit
assert_exception_class(subtests, MyError)

# 2. Přísná shoda textových defaultů (Exact match)
assert_exception_class(subtests, MyError, exact_match=True)

# 3. Kontrola pouze začátku textu (Prefix match)
assert_exception_class(subtests, MyError, startswith=True)

# 4. Tichý režim bez pytest subtestů
assert_exception_class(subtests, MyError, verbose=False)

# 5. Rychlý základní test (bez kontroly konstruktoru a API)
assert_exception_class(subtests, MyError, deep_check=False)