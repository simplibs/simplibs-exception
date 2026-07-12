# 📦 `_core_logic/tracing` — Location Tracing Engine

Balíček `tracing` obsahuje interní mechanismy, které určují **kde** výjimka vznikla.  
Je to základní stavební kámen pro všechny výstupní režimy (`PRETTY`, `SIMPLE`, `LOG`, `ONELINE`)  
a pro funkce jako `with_location_offset()`.

Je navržen tak, aby byl:

- **deterministický**,  
- **cross‑platform**,  
- **bezpečný** (Do‑No‑Harm),  
- **plně izolovaný od zbytku knihovny**,  
- **odolný vůči refaktorům**.

---

## 🧭 Co tento balíček řeší?

### 1) Určení správného místa vzniku výjimky  
Když uživatel vyvolá `SimpleException`, knihovna musí najít:

- soubor,  
- cestu,  
- řádek,  
- funkci,  

kde chyba skutečně vznikla — **ne** místo uvnitř knihovny.

### 2) Přeskakování interních rámců  
Knihovna má mnoho interních vrstev.  
Uživatel nechce vidět:

- wrapper funkce,  
- utility funkce,  
- interní logiku knihovny.

Proto existuje:

- `skip_locations`  
- `expected_frames`  
- `with_location_offset()`  

Tyto mechanismy společně určují, **který stack frame je ten správný**.

### 3) Re‑raise bez ztráty kontextu  
Pokud knihovna zachytí výjimku a znovu ji vyvolá, musí být výstupní místo:

- **uživatelův kód**,  
- ne interní wrapper.

K tomu slouží `with_location_offset()`.

---

## 📁 Obsah balíčku

### `extract_caller_info.py`
Funkce, která:

- prochází stack,  
- filtruje interní rámce podle `excluded_patterns`,  
- normalizuje cesty na POSIX,  
- vrací metadata o vybraném rámci,  
- nikdy nevyvolá výjimku (Do‑No‑Harm).

Je to **jediný zdroj pravdy** pro získání informací o místě vzniku chyby.

---

### `with_location_offset.py`
Funkce, která:

- vytvoří **novou instanci** výjimky,  
- zvýší hloubku `get_location`,  
- umožní přeskočit wrapper funkce při re‑raise,  
- zachová všechny ostatní atributy (včetně UNSET).

Používá se přes metodu:

```python
exc.with_location_offset(offset=1)
```

---

### `__init__.py`
Pouze re-exporty, aby balíček poskytoval čisté API.

---

## 🧩 Jak tracing zapadá do celého systému?

Tracing je úzce propojen s:

- `SimpleExceptionData.caller_info`  
- `process_get_location()`  
- `process_skip_locations()`  
- výstupními režimy (`PRETTY`, `SIMPLE`, `LOG`, `ONELINE`)  

Ale **není** propojen s:

- MRO logikou,  
- normalizačními funkcemi,  
- serializací,  
- layout enginem.

Je to izolovaný modul, který řeší jedinou věc:  
**Najít správný stack frame.**

---

## 🔍 Příklady použití

### Základní výjimka
```python
raise SimpleException("Boom!", label="x")
```

Výstup bude obsahovat místo, kde byla výjimka vyvolána.

---

### Přeskakování wrapperu
```python
def wrapper():
    try:
        do_something()
    except SimpleException as exc:
        raise exc.with_location_offset(1)
```

Uživatel uvidí místo v `do_something()`, ne ve `wrapper()`.

---

### Vypnutí tracingu
```python
raise SimpleException("Boom", get_location=False)
```

Výstup nebude obsahovat žádné informace o souboru/řádku.

---

## 🛡️ Architektonické principy

- **Do‑No‑Harm**  
  Tracing nikdy nesmí způsobit další chybu.

- **Cross‑Platform**  
  Všechny cesty jsou normalizovány na POSIX.

- **Content‑Based Filtering**  
  Nepracuje s pevnými offsety, ale s blacklistem cest.

- **Safety Net**  
  Pokud je blacklist příliš agresivní, vrací poslední dostupný rámec.

- **Immutabilita**  
  `with_location_offset()` nikdy nemění existující instanci.

---