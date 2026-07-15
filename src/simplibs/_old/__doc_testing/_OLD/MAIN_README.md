# 📦 `simplibs.exception.testing` — Unifikovaný testovací framework

Tento balíček poskytuje kompletní, modulární a automatizovanou infrastrukturu pro testování ekosystému `SimpleException`. Umožňuje eliminovat duplicitní kód v testech a pokrýt celou architekturu od definic tříd až po komplexní validační funkce a celé subsystémy.

---

## 🗺️ Architektonické vrstvy frameworku

Testovací nástroje jsou rozděleny do tří logických vrstev podle komplexnosti:

```text
  ┌──────────────────────────────────────────────────────────┐
    1. MATICOVÁ VRSTVA (Hromadné testy subsystémů)            
       ➔ bulk_test (exceptions_bulk_test) + FuncCase          
  └────────────────────────────┬─────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────┐
    2. KOMPOZITNÍ ORCHESTRÁTORY (Ucelené testy komponent)    
       ➔ assert_exception_class  
       ➔ assert_exception_function  
  └────────────────────────────┬─────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────┐
    3. ASSERT FUNKCE (Testování jednotlivých okruhů)    
       ➔ assert_class_constructor
       ➔ assert_class_defaults
       ➔ assert_class_inheritance
       ➔ assert_class_interface
       ➔ assert_function_callable
       ➔ assert_function_raises
       ➔ assert_function_valid_input
       ➔ assert_exception_fields
  └────────────────────────────┬─────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────┐
    4. POMOCNÉ NÁSTROJE & ATOMICKÉ KONTROLY                   
       ➔ tools (Kwargs, maybe_subtest)                        
  └──────────────────────────────────────────────────────────┘

```

---

## 🧭 Rozcestník komponent & Dokumentace

### 1. Kompozitní orchestrátory (Úroveň komponent)

* **`assert_exception_class` — Audit tříd výjimek**
* **Co dělá:** Provádí kompletní strukturální kontrolu tříd (dědičnost, defaultní hodnoty polí, chování konstruktoru, serializace).
* 📄 **Více viz zde:** `[TODO: Doplňte cestu k README_CLASS / assert_exception_class.md]`


* **`assert_exception_function` — Audit funkční logiky**
* **Co dělá:** Ověřuje, že testovaná funkce správně reaguje na validní vstupech a při nevalidních datech vyvolá přesný typ výjimky včetně detailní kontroly jejích polí.
* 📄 **Více viz zde:** `[TODO: Doplňte cestu k README_FUNCTION / assert_exception_function.md]`



---

### 2. Maticové testování (Úroveň celých subsystémů)

* **`exceptions_bulk_test` — Hromadný maticový runner**
* **Co dělá:** Spouští celé matice testů složené z definic tříd, inline funkcí a komplexních případů najednou. Automaticky směruje položky do správných auditorů.
* 📄 **Více viz zde:** `[TODO: Doplňte cestu k README / USER_GUIDE pro bulk_test]`


* **`FuncCase` — Deklarativní testovací scénář**
* **Co dělá:** Slouží jako čistě datový kontejner pro popis jednoho uceleného testu funkce a očekávaných telemetrických dat vyvolané výjimky.
* 📄 **Více viz zde:** `[TODO: Doplňte cestu k USER_GUIDE pro FuncCase]`



---

### 3. Pomocné testovací nástroje (Utility)

* **`Kwargs` — Sémantický wrapper parametrů**
* **Co dělá:** Bezpečně odlišuje standardní slovník (hodnotu) od pojmenovaných parametrů (`kwargs`) předávaných do testovaných funkcí.
* 📄 **Více viz zde:** `[TODO: Doplňte cestu k USER_GUIDE pro Kwargs]`


* **`maybe_subtest` — Podmíněný context manager**
* **Co dělá:** Odstraňuje větvení kódu v testech. Umožňuje plynule přepínat mezi upovídaným režimem s pytest subtesty (`verbose=True`) a rychlým tichým režimem (`verbose=False`).
* 📄 **Více viz zde:** `[TODO: Doplňte cestu k USER_GUIDE pro maybe_subtest]`



---

## 🛡️ Klíčové přínosy frameworku

1. **Žádný duplicitní kód:** Test celého složitého subsystému se smrskne do jediné čitelné datové tabulky (matice).
2. **Fail-Fast & Determinismus:** Pipeline kroků má pevný řád. Chyby jsou odhalovány okamžitě v prvním bodě selhání.
3. **Podpora pro CI/CD (Shallow/Deep):** Možnost globálně přepnout testy do rychlého kouřového režimu pro rychlé CI/CD builds, nebo spustit hluboký strukturální audit.