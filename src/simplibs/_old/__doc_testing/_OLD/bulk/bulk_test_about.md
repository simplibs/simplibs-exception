# 📦 `bulk_test` — Automatizované maticové testování subsystémů

Balíček `bulk_test` poskytuje nejvyšší vrstvu testovacího frameworku `SimpleException`. Tento automatizovaný orchestrátor umožňuje psát **jediný test**, který kompletně pokryje celou architekturu (třídy výjimek, testovací funkce i komplexní scénáře).

> 💡 **Hledáte podrobný návod a praktickou kuchařku?** Přejděte na [Uživatelský průvodce s příklady](USER_GUIDE.md).

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

## 🎛️ Přehled konfigurace orchestrátoru

- `deep_check=True` ➔ **Hluboký audit:** Vynutí kompletní validaci tříd (konstruktory, serializace) a hloubkovou kontrolu polí u `FuncCase`.
- `deep_check=False` ➔ **Rychlý test:** Kontroluje pouze základní záchyt výjimek, správnost typů a základní defaulty tříd. Ideální pro rychlou zpětnou vazbu.
- `verbose=True` ➔ Každý dílčí prvek a každé kontrolované pole v matici se spustí jako samostatný pytest `subtest`.

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

