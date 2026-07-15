# 📦 `testing/asserts/fields` 
**Field-Level Exception Assertion Engine**

Balíček `asserts/fields` obsahuje základní stavební kámen celé testovací infrastruktury knihovny **SimpleException**:  
**granulární validátor jednotlivých polí výjimky**.

Je to nejnižší úroveň testovacího systému, na které staví:

- `assert_exception_class` (testování tříd výjimek),  
- `assert_exception_function` (testování funkcí, které výjimky vyvolávají),  
- `bulk_test` (automatické generování testů),  
- všechny vyšší testovací pipelines.

---
## 📁 Obsah balíčku

### `assert_exception_fields.py`

## 🧭 Co tento kod řeší?

### 1) Granulární validaci jednotlivých atributů výjimky
Každá výjimka má množinu atributů:

- `error_name`  
- `label`  
- `message`  
- `expected`  
- `value`  
- `problem`  
- `context`  
- `how_to_fix`  
- `exception`  
- `get_location`  
- `skip_locations`  
- `oneline`

`assert_exception_fields` umožňuje **selektivně** validovat libovolnou podmnožinu těchto atributů.

To je zásadní, protože:

- některé testy kontrolují jen jeden atribut,  
- některé kontrolují všechny,  
- některé kontrolují jen změny oproti defaultům,  
- některé kontrolují jen runtime chování.

---

### 2) Podpora fuzzy, prefix a exact match porovnání
Textové atributy (např. `message`, `problem`, `context`) mohou být:

- dynamické,  
- víceliniové,  
- generované layout enginem,  
- obsahovat metadata,  
- obsahovat stack trace.

Proto balíček poskytuje tři režimy porovnání:

- **exact_match=True** → striktní rovnost  
- **startswith=True** → prefix match  
- **default** → fuzzy substring match  

Tím se testy stávají robustními a ne-křehkými.

---

### 3) Podmíněné subtesty (`maybe_subtest`)
Každý atribut může být validován:

- v samostatném subtestu (verbose režim),  
- nebo bez subtestu (silent režim).

To umožňuje:

- čisté výpisy při vývoji,  
- rychlé běhy v CI,  
- přehledné oddělení chyb.

---

### 4) Normalizaci hodnot (`_normalize_value`)
Textové hodnoty mohou být:

- `None`,  
- `UNSET`,  
- tuple,  
- string,  
- libovolný objekt.

Normalizace zajišťuje:

- konzistentní porovnání,  
- bezpečné operace nad stringy,  
- jednotné chování napříč typy.

---

### 5) Porovnání textů (`compare_strings`)
Tato funkce je jádrem textové validace:

- provádí fuzzy match, prefix match nebo exact match,  
- používá normalizaci,  
- je deterministická a jednoduchá.

---

## 🔍 Příklady použití

### Validace jednoho atributu
```python
assert_exception_fields(subtests, exc, message="Boom")
```

### Validace více atributů
```python
assert_exception_fields(
    subtests,
    exc,
    error_name="VALUE_ERROR",
    label="user_id",
    expected="non-empty",
    exact_match=True,
)
```

### Prefix match
```python
assert_exception_fields(subtests, exc, message="Invalid", startswith=True)
```

### Fuzzy match
```python
assert_exception_fields(subtests, exc, problem="token")
```

### Silent režim
```python
assert_exception_fields(subtests, exc, message="Boom", verbose=False)
```
